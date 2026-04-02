import ipfshttpclient
import json
import os

# 连接本地IPFS节点（需提前启动IPFS服务）
client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001/http")

def upload_nft_image(image_path: str) -> str:
    """上传NFT图片至IPFS，返回图片IPFS哈希"""
    if not os.path.exists(image_path):
        raise FileNotFoundError("图片文件不存在")
    # 上传图片
    res = client.add(image_path)
    return res["Hash"]

def create_nft_metadata(image_hash: str, name: str, description: str, attributes: list) -> dict:
    """创建符合ERC721标准的NFT元数据"""
    metadata = {
        "name": name,
        "description": description,
        "image": f"ipfs://{image_hash}",
        "attributes": attributes
    }
    return metadata

def upload_nft_metadata(metadata: dict) -> str:
    """上传NFT元数据至IPFS，返回元数据URI"""
    # 将元数据转换为JSON字符串
    metadata_json = json.dumps(metadata, indent=4)
    # 上传JSON数据（以字符串形式上传）
    res = client.add(metadata_json.encode("utf-8"))
    return f"ipfs://{res['Hash']}"

def batch_upload_nft_metadata(metadata_list: list) -> list:
    """批量上传NFT元数据，返回所有元数据URI"""
    uris = []
    for metadata in metadata_list:
        uri = upload_nft_metadata(metadata)
        uris.append(uri)
    return uris

if __name__ == "__main__":
    # 测试单张NFT元数据上传
    image_hash = upload_nft_image("nft_image.png")  # 替换为本地图片路径
    print(f"图片IPFS哈希：{image_hash}")
    
    nft_metadata = create_nft_metadata(
        image_hash=image_hash,
        name="Web3 Advanced NFT",
        description="区块链进阶实战NFT，用于GitHub技术展示",
        attributes=[{"trait_type": "Technology", "value": "Web3"}, {"trait_type": "Type", "value": "Practice"}]
    )
    
    metadata_uri = upload_nft_metadata(nft_metadata)
    print(f"NFT元数据URI：{metadata_uri}")
