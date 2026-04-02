from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64

def aes_encrypt(data: str, password: str) -> str:
    # 生成盐值和IV
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)
    # 生成密钥
    key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
    # AES加密（CBC模式）
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 填充数据（满足AES块大小要求）
    padding_length = AES.block_size - len(data.encode()) % AES.block_size
    data_padded = data.encode() + (chr(padding_length) * padding_length).encode()
    ciphertext = cipher.encrypt(data_padded)
    # 拼接盐值、IV和密文，base64编码
    return base64.b64encode(salt + iv + ciphertext).decode()

def aes_decrypt(encrypted_data: str, password: str) -> str:
    # 解码并拆分盐值、IV和密文
    data = base64.b64decode(encrypted_data)
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]
    # 生成密钥
    key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
    # AES解密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    # 去除填充
    padding_length = plaintext_padded[-1]
    plaintext = plaintext_padded[:-padding_length].decode()
    return plaintext

if __name__ == "__main__":
    # 测试：加密私钥
    private_key = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    password = "web3_secure_password_123"
    
    encrypted = aes_encrypt(private_key, password)
    print(f"加密后私钥: {encrypted}")
    
    decrypted = aes_decrypt(encrypted, password)
    print(f"解密后私钥: {decrypted}")
