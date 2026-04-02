from web3 import Web3
from solders.rpc import rpc_request
import time
import smtplib
from email.mime.text import MIMEText

class BlockchainNodeMonitor:
    def __init__(self, eth_rpc: str, sol_rpc: str, alert_email: str = None, smtp_server: str = "smtp.163.com", smtp_port: int = 25, smtp_user: str = None, smtp_pass: str = None):
        # 初始化节点连接
        self.eth_w3 = Web3(Web3.HTTPProvider(eth_rpc))
        self.sol_rpc = sol_rpc
        # 告警配置
        self.alert_email = alert_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        # 历史数据（用于计算出块速度）
        self.last_eth_block = None
        self.last_eth_time = None

    def send_alert(self, subject: str, content: str):
        """发送邮件告警"""
        if not all([self.alert_email, self.smtp_user, self.smtp_pass]):
            print("⚠️  未配置邮件信息，无法发送告警")
            return
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = self.alert_email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            print("✅ 告警邮件已发送")
        except Exception as e:
            print(f"❌ 告警邮件发送失败：{str(e)}")

    def check_eth_node(self):
        """检查以太坊节点健康状态"""
        status = {
            "chain": "Ethereum",
            "connected": False,
            "latest_block": None,
            "sync_status": "Unknown",
            "block_time": None,
            "healthy": False
        }
        try:
            # 检查连接状态
            if self.eth_w3.is_connected():
                status["connected"] = True
                current_block = self.eth_w3.eth.block_number
                status["latest_block"] = current_block
                # 检查同步状态（假设最新区块与本地节点区块差≤3为同步正常）
                public_block = self.eth_w3.eth.get_block("latest")["number"]
                status["sync_status"] = "Synced" if abs(current_block - public_block) ≤ 3 else "Not Synced"
                # 计算出块速度
                current_time = time.time()
                if self.last_eth_block and self.last_eth_time:
                    if current_block > self.last_eth_block:
                        block_count = current_block - self.last_eth_block
                        time_diff = current_time - self.last_eth_time
                        status["block_time"] = time_diff / block_count
                # 更新历史数据
                self.last_eth_block = current_block
                self.last_eth_time = current_time
                # 判断健康状态
                status["healthy"] = status["connected"] and status["sync_status"] == "Synced"
            else:
                self.send_alert("以太坊节点告警", "以太坊节点连接失败，请检查节点状态！")
        except Exception as e:
            status["error"] = str(e)
            self.send_alert("以太坊节点告警", f"以太坊节点检查失败：{str(e)}")
        return status

    def check_sol_node(self):
        """检查Solana节点健康状态（简化版）"""
        status = {
            "chain": "Solana",
            "connected": False,
            "latest_block": None,
            "healthy": False
        }
        try:
            # 调用Solana RPC获取最新区块
            response = rpc_request(self.sol_rpc, "getSlot", [])
            if response["result"]:
                status["connected"] = True
                status["latest_block"] = response["result"]
                status["healthy"] = True
            else:
                self.send_alert("Solana节点告警", "Solana节点连接失败，请检查节点状态！")
        except Exception as e:
            status["error"] = str(e)
            self.send_alert("Solana节点告警", f"Solana节点检查失败：{str(e)}")
        return status

    def monitor(self, interval: int = 60):
        """持续监控节点状态（每隔interval秒检查一次）"""
        print(f"🚀 区块链节点监控启动，检查间隔：{interval}秒")
        while True:
            eth_status = self.check_eth_node()
            sol_status = self.check_sol_node()
            print(f"\n【{time.strftime('%Y-%m-%d %H:%M:%S')}】节点状态报告")
            print(f"以太坊：{eth_status}")
            print(f"Solana：{sol_status}")
            time.sleep(interval)

if __name__ == "__main__":
    # 测试节点监控
    monitor = BlockchainNodeMonitor(
        eth_rpc="https://eth.llamarpc.com",
        sol_rpc="https://api.mainnet-beta.solana.com",
        # 请替换为实际邮件配置（可选）
        alert_email="your_email@163.com",
        smtp_user="your_email@163.com",
        smtp_pass="your_email_password"
    )
    monitor.monitor(interval=300)  # 每5分钟检查一次
