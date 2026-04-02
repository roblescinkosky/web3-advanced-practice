// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// 标准ERC1155多代币合约
contract ERC1155MultiToken {
    // 代币名称和符号
    string public name = "Web3 Advanced MultiToken";
    string public symbol = "W3AMT";

    // 余额映射：address -> tokenId -> 余额
    mapping(address => mapping(uint256 => uint256)) private _balances;
    // 授权映射：owner -> spender -> tokenId -> 授权数量
    mapping(address => mapping(address => mapping(uint256 => uint256))) private _allowances;

    // 事件定义
    event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 indexed id, uint256 value);
    event TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] indexed ids, uint256[] values);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    // 余额查询
    function balanceOf(address account, uint256 id) public view returns (uint256) {
        require(account != address(0), "Invalid account");
        return _balances[account][id];
    }

    // 批量余额查询
    function balanceOfBatch(address[] calldata accounts, uint256[] calldata ids) public view returns (uint256[] memory) {
        require(accounts.length == ids.length, "Accounts and ids length mismatch");
        uint256[] memory balances = new uint256[](accounts.length);
        for (uint256 i = 0; i < accounts.length; i++) {
            balances[i] = balanceOf(accounts[i], ids[i]);
        }
        return balances;
    }

    // 授权单个代币
    function setApprovalForAll(address operator, bool approved) public {
        require(operator != address(0), "Invalid operator");
        _allowances[msg.sender][operator][0] = approved ? type(uint256).max : 0;
        emit ApprovalForAll(msg.sender, operator, approved);
    }

    // 检查授权
    function isApprovedForAll(address owner, address operator) public view returns (bool) {
        return _allowances[owner][operator][0] == type(uint256).max;
    }

    // 单个代币转账
    function transferFrom(address from, address to, uint256 id, uint256 value) public {
        require(from != address(0) && to != address(0), "Invalid address");
        require(value > 0, "Value must be positive");
        // 检查授权（本人或已授权）
        require(msg.sender == from || isApprovedForAll(from, msg.sender), "Not authorized");
        require(_balances[from][id] >= value, "Insufficient balance");

        _balances[from][id] -= value;
        _balances[to][id] += value;
        emit TransferSingle(msg.sender, from, to, id, value);
    }

    // 批量代币转账
    function safeBatchTransferFrom(address from, address to, uint256[] calldata ids, uint256[] calldata values, bytes calldata data) public {
        require(from != address(0) && to != address(0), "Invalid address");
        require(ids.length == values.length, "Ids and values length mismatch");
        require(msg.sender == from || isApprovedForAll(from, msg.sender), "Not authorized");

        for (uint256 i = 0; i < ids.length; i++) {
            uint256 id = ids[i];
            uint256 value = values[i];
            require(_balances[from][id] >= value, "Insufficient balance for id");
            _balances[from][id] -= value;
            _balances[to][id] += value;
        }
        emit TransferBatch(msg.sender, from, to, ids, values);
    }

    //  mint单个代币
    function mint(address to, uint256 id, uint256 value) public {
        require(to != address(0), "Invalid address");
        require(value > 0, "Value must be positive");

        _balances[to][id] += value;
        emit TransferSingle(msg.sender, address(0), to, id, value);
    }

    // 批量mint代币
    function mintBatch(address to, uint256[] calldata ids, uint256[] calldata values) public {
        require(to != address(0), "Invalid address");
        require(ids.length == values.length, "Ids and values length mismatch");

        for (uint256 i = 0; i < ids.length; i++) {
            uint256 id = ids[i];
            uint256 value = values[i];
            require(value > 0, "Value must be positive");
            _balances[to][id] += value;
        }
        emit TransferBatch(msg.sender, address(0), to, ids, values);
    }

    // 销毁代币
    function burn(address from, uint256 id, uint256 value) public {
        require(from != address(0), "Invalid address");
        require(value > 0, "Value must be positive");
        require(msg.sender == from || isApprovedForAll(from, msg.sender), "Not authorized");
        require(_balances[from][id] >= value, "Insufficient balance");

        _balances[from][id] -= value;
        emit TransferSingle(msg.sender, from, address(0), id, value);
    }
}
