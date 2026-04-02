from web3 import Web3
import json

# 连接以太坊RPC节点
RPC_URL = "https://eth.llamarpc.com"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def crawl_transactions(address: str, output_file: str = "transactions.json"):
    if not w3.is_address(address):
        raise ValueError("无效的以太坊地址")
    
    transactions = []
    # 从最新区块开始往前查询（可调整查询范围）
    latest_block = w3.eth.block_number
    start_block = latest_block - 100  # 查询最近100个区块的交易
    
    for block_num in range(start_block, latest_block + 1):
        block = w3.eth.get_block(block_num, full_transactions=True)
        for tx in block.transactions:
            # 筛选涉及目标地址的交易（发送或接收）
            if tx["from"] == address.lower() or tx["to"] == address.lower():
                tx_info = {
                    "block_number": block_num,
                    "transaction_hash": w3.to_hex(tx["hash"]),
                    "from_address": tx["from"],
                    "to_address": tx["to"],
                    "value_eth": w3.from_wei(tx["value"], "ether"),
                    "gas_used": tx["gas"],
                    "gas_price_gwei": w3.from_wei(tx["gasPrice"], "gwei"),
                    "input_data": w3.to_hex(tx["input"]),
                    "status": w3.eth.get_transaction_receipt(tx["hash"])["status"]
                }
                transactions.append(tx_info)
    
    # 导出为JSON文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4)
    
    print(f"交易抓取完成，共{len(transactions)}笔交易，已保存至{output_file}")
    return transactions

if __name__ == "__main__":
    # 测试：抓取指定地址交易
    test_address = "0x1234567890123456789012345678901234567890"
    crawl_transactions(test_address)
