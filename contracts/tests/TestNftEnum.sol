// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "../enumerable/ERC721xEnum.sol";

contract TestNFTEnum is ERC721xEnum("", "") {
	function mint(uint256 _id) external {
		_mint(msg.sender, _id);
	}
}