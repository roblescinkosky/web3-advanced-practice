// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ContractSecurityChecker {
    // 重入攻击检测标记
    bool private _reentrancyGuard;
    // 权限控制标记（仅拥有者可操作）
    address private _owner;

    event VulnerabilityDetected(string vulnerabilityType, string message);

    constructor() {
        _owner = msg.sender;
    }

    // 重入防护修饰器
    modifier nonReentrant() {
        require(!_reentrancyGuard, "Reentrancy detected");
        _reentrancyGuard = true;
        _;
        _reentrancyGuard = false;
    }

    // 权限控制修饰器
    modifier onlyOwner() {
        require(msg.sender == _owner, "Not owner");
        _;
    }

    // 整数溢出/下溢检测（0.8.0+默认检查，此处做额外校验）
    function safeAdd(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result = a + b;
        require(result >= a && result >= b, "Integer overflow detected");
        return result;
    }

    function safeSub(uint256 a, uint256 b) public pure returns (uint256) {
        require(b <= a, "Integer underflow detected");
        return a - b;
    }

    // 示例：带安全校验的转账函数
    function transfer(address to, uint256 amount) external nonReentrant onlyOwner {
        require(to != address(0), "Invalid address");
        require(amount > 0, "Amount must be positive");
        // 此处可添加实际转账逻辑，示例仅做安全校验演示
        emit VulnerabilityDetected("None", "Transfer executed safely");
    }

    // 权限检查接口
    function checkOwner(address account) external view returns (bool) {
        return account == _owner;
    }

    // 重入状态检查接口
    function checkReentrancyStatus() external view returns (bool) {
        return _reentrancyGuard;
    }
}
