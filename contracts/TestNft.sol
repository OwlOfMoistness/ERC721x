// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "./Erc721LockRegistry.sol";

contract TestNFT is Erc721LockRegistry("", "") {
	function mint(uint256 _id) external {
		_mint(msg.sender, _id);
	}
}