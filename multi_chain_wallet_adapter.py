from web3 import Web3
from solders.keypair import Keypair
from base58 import b58encode, b58decode
import hashlib

class MultiChainWallet:
    def __init__(self):
        # 初始化各公链节点连接
        self.eth_w3 = Web3(Web3.HTTPProvider("https://eth.llamarpc.com"))
        self.polygon_w3 = Web3(Web3.HTTPProvider("https://polygon.llamarpc.com"))

    # 以太坊钱包操作
    def eth_generate_wallet(self):
        account = self.eth_w3.eth.account.create()
        return {
            "chain": "Ethereum",
            "address": account.address,
            "private_key": account.key.hex()
        }

    def eth_get_balance(self, address: str):
        if not self.eth_w3.is_address(address):
            return None
        return self.eth_w3.from_wei(self.eth_w3.eth.get_balance(address), "ether")

    # Solana钱包操作
    def sol_generate_wallet(self):
        keypair = Keypair()
        return {
            "chain": "Solana",
            "address": str(keypair.pubkey()),
            "private_key": b58encode(keypair.secret()).decode()
        }

    # Polygon钱包操作（与以太坊兼容，单独封装接口）
    def polygon_get_balance(self, address: str):
        if not self.polygon_w3.is_address(address):
            return None
        return self.polygon_w3.from_wei(self.polygon_w3.eth.get_balance(address), "ether")

    # 批量生成多链钱包
    def batch_generate_wallets(self, chain: str, count: int = 5):
        wallets = []
        if chain.lower() == "ethereum":
            for _ in range(count):
                wallets.append(self.eth_generate_wallet())
        elif chain.lower() == "solana":
            for _ in range(count):
                wallets.append(self.sol_generate_wallet())
        elif chain.lower() == "polygon":
            for _ in range(count):
                wallets.append(self.eth_generate_wallet())  # Polygon与ETH地址生成逻辑一致
        return wallets

if __name__ == "__main__":
    wallet = MultiChainWallet()
    
    # 测试单链钱包生成
    eth_wallet = wallet.eth_generate_wallet()
    print("以太坊钱包：", eth_wallet)
    
    sol_wallet = wallet.sol_generate_wallet()
    print("Solana钱包：", sol_wallet)
    
    # 测试批量生成
    batch_eth = wallet.batch_generate_wallets("ethereum", 3)
    print("批量生成以太坊钱包：", batch_eth)
