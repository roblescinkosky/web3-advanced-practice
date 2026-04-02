import hashlib
import math

# SECP256K1曲线参数（区块链标准参数）
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0x0000000000000000000000000000000000000000000000000000000000000000
B = 0x0000000000000000000000000000000000000000000000000000000000000007
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def mod_inverse(a, m):
    """模逆计算（扩展欧几里得算法）"""
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += m0
    return x

def point_add(p1, p2):
    """椭圆曲线点加法"""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and y1 == y2:
        # 点加倍
        s = (3 * x1 * x1 + A) * mod_inverse(2 * y1, P) % P
    else:
        # 不同点加法
        s = (y2 - y1) * mod_inverse(x2 - x1, P) % P
    x3 = (s * s - x1 - x2) % P
    y3 = (s * (x1 - x3) - y1) % P
    return (x3, y3)

def point_multiply(p, k):
    """椭圆曲线点乘法（快速幂算法）"""
    result = None
    while k > 0:
        if k % 2 == 1:
            result = point_add(result, p)
        p = point_add(p, p)
        k = k // 2
    return result

def generate_key_pair():
    """生成SECP256K1密钥对（私钥+公钥）"""
    # 生成随机私钥（1 < 私钥 < N）
    private_key = int(hashlib.sha256(os.urandom(32)).hexdigest(), 16) % (N - 1) + 1
    # 计算公钥（G * 私钥）
    public_key = point_multiply((Gx, Gy), private_key)
    return {
        "private_key": hex(private_key)[2:].zfill(64),  # 64位十六进制私钥
        "public_key": (hex(public_key[0])[2:].zfill(64), hex(public_key[1])[2:].zfill(64))
    }

def sign_message(private_key: str, message: str):
    """签名消息（SHA256哈希后签名）"""
    priv_key = int(private_key, 16)
    # 哈希消息
    msg_hash = hashlib.sha256(message.encode()).digest()
    msg_hash_int = int.from_bytes(msg_hash, byteorder="big") % N
    # 生成随机数k
    k = int(hashlib.sha256(os.urandom(32)).hexdigest(), 16) % (N - 1) + 1
    # 计算r = (G*k).x mod N
    r = point_multiply((Gx, Gy), k)[0] % N
    # 计算s = (msg_hash_int + priv_key * r) * k^{-1} mod N
    s = (msg_hash_int + priv_key * r) * mod_inverse(k, N) % N
    return (hex(r)[2:].zfill(64), hex(s)[2:].zfill(64))

if __name__ == "__main__":
    # 测试密钥对生成与签名
    key_pair = generate_key_pair()
    print("私钥：", key_pair["private_key"])
    print("公钥（x,y）：", key_pair["public_key"])
    
    message = "Web3 SECP256K1 Signature Test"
    signature = sign_message(key_pair["private_key"], message)
    print("消息签名：", signature)
