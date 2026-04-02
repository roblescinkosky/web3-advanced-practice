from web3 import Web3
from web3.middleware import geth_poa_middleware

# 连接Arbitrum Layer2节点（公开节点）
ARBITRUM_RPC = "https://arbitrum-one.public.blastapi.io"
w3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC))
# 添加POA中间件（Arbitrum为POA网络）
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

def connect_arbitrum():
    """检查Arbitrum节点连接状态"""
    if w3.is_connected():
        print(f"✅ 已连接Arbitrum Layer2，最新区块：{w3.eth.block_number}")
        return True
    else:
        print("❌ Arbitrum节点连接失败")
        return False

def get_arbitrum_balance(address: str):
    """查询Arbitrum上指定地址的ETH余额"""
    if not w3.is_address(address):
        return "无效地址"
    balance_wei = w3.eth.get_balance(address)
    return w3.from_wei(balance_wei, "ether")

def arbitrum_contract_interaction(contract_addr: str, abi: list, function_name: str, *args):
    """Arbitrum上合约交互"""
    if not connect_arbitrum():
        return
    contract = w3.eth.contract(address=contract_addr, abi=abi)
    # 调用合约只读方法（无需交易）
    try:
        result = getattr(contract.functions, function_name)(*args).call()
        print(f"合约交互结果：{result}")
        return result
    except Exception as e:
        print(f"合约交互失败：{str(e)}")
        return None

if __name__ == "__main__":
    # 测试连接与余额查询
    connect_arbitrum()
    test_address = "0x1234567890123456789012345678901234567890"
    print(f"地址{test_address}的Arbitrum ETH余额：{get_arbitrum_balance(test_address)} ETH")
    
    # 示例：查询Arbitrum上USDT合约余额（ABI仅保留balanceOf方法）
    usdt_abi = [{"constant":True,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"}]
    usdt_addr = "0xFd086bC7CD5C481DCC9C854C9d68f989508577D3"
    arbitrum_contract_interaction(usdt_addr, usdt_abi, "balanceOf", test_address)
