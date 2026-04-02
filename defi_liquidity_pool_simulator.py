class DeFiLiquidityPool:
    def __init__(self, token_a_name: str, token_b_name: str, fee_rate: float = 0.003):
        # 初始化流动性池
        self.token_a = token_a_name  # 代币A名称
        self.token_b = token_b_name  # 代币B名称
        self.fee_rate = fee_rate     # 交易手续费率（默认0.3%）
        self.reserve_a = 0.0         # 代币A储备量
        self.reserve_b = 0.0         # 代币B储备量
        self.total_liquidity = 0.0   # 总流动性代币数量
        self.liquidity_providers = {}  # 流动性提供者（地址: 流动性代币数量）

    def add_liquidity(self, lp_address: str, amount_a: float, amount_b: float):
        """添加流动性"""
        if amount_a <= 0 or amount_b <= 0:
            raise ValueError("添加的代币数量必须大于0")
        
        # 首次添加流动性，初始化储备量和流动性代币
        if self.total_liquidity == 0:
            # 流动性代币数量 = 储备量乘积的平方根（简化模型）
            liquidity = math.sqrt(amount_a * amount_b)
        else:
            # 非首次添加，按比例计算可获得的流动性代币
            liquidity = min(
                (amount_a / self.reserve_a) * self.total_liquidity,
                (amount_b / self.reserve_b) * self.total_liquidity
            )
        
        # 更新储备量和流动性代币
        self.reserve_a += amount_a
        self.reserve_b += amount_b
        self.total_liquidity += liquidity
        self.liquidity_providers[lp_address] = self.liquidity_providers.get(lp_address, 0.0) + liquidity
        
        print(f"✅ 成功添加流动性：{amount_a} {self.token_a} + {amount_b} {self.token_b}")
        print(f"获得流动性代币：{liquidity:.4f}，总流动性：{self.total_liquidity:.4f}")
        return liquidity

    def remove_liquidity(self, lp_address: str, liquidity_amount: float):
        """移除流动性"""
        lp_liquidity = self.liquidity_providers.get(lp_address, 0.0)
        if liquidity_amount <= 0 or liquidity_amount > lp_liquidity:
            raise ValueError("流动性代币数量无效")
        
        # 按比例计算可提取的代币数量
        amount_a = (liquidity_amount / self.total_liquidity) * self.reserve_a
        amount_b = (liquidity_amount / self.total_liquidity) * self.reserve_b
        
        # 更新储备量和流动性代币
        self.reserve_a -= amount_a
        self.reserve_b -= amount_b
        self.total_liquidity -= liquidity_amount
        self.liquidity_providers[lp_address] -= liquidity_amount
        
        print(f"✅ 成功移除流动性：{liquidity_amount:.4f} 流动性代币")
        print(f"提取代币：{amount_a:.4f} {self.token_a} + {amount_b:.4f} {self.token_b}")
        return (amount_a, amount_b)

    def swap(self, token_in: str, amount_in: float):
        """代币兑换（AMM机制：储备量乘积恒定）"""
        if amount_in <= 0:
            raise ValueError("兑换的代币数量必须大于0")
        if token_in not in [self.token_a, self.token_b]:
            raise ValueError("不支持的代币类型")
        
        # 计算可兑换的代币数量（扣除手续费）
        amount_in_with_fee = amount_in * (1 - self.fee_rate)
        if token_in == self.token_a:
            amount_out = (amount_in_with_fee * self.reserve_b) / (self.reserve_a + amount_in_with_fee)
            # 更新储备量
            self.reserve_a += amount_in
            self.reserve_b -= amount_out
            print(f"✅ 兑换成功：{amount_in} {self.token_a} → {amount_out:.4f} {self.token_b}（手续费：{amount_in * self.fee_rate:.4f} {self.token_a}）")
            return amount_out
        else:
            amount_out = (amount_in_with_fee * self.reserve_a) / (self.reserve_b + amount_in_with_fee)
            # 更新储备量
            self.reserve_b += amount_in
            self.reserve_a -= amount_out
            print(f"✅ 兑换成功：{amount_in} {self.token_b} → {amount_out:.4f} {self.token_a}（手续费：{amount_in * self.fee_rate:.4f} {self.token_b}）")
            return amount_out

if __name__ == "__main__":
    # 测试流动性池运作
    pool = DeFiLiquidityPool("ETH", "USDT", 0.003)
    
    # 添加流动性
    pool.add_liquidity("0x123", 10.0, 20000.0)
    
    # 代币兑换
    pool.swap("ETH", 1.0)
    
    # 移除流动性
    pool.remove_liquidity("0x123", 10.0)
