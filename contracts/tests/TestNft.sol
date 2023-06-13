// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "../ERC721x.sol";

contract TestNFT is ERC721x("", "") {
	function mint(uint256 _id) external {
		_mint(msg.sender, _id);
	}
}