// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "../enumerable/ERC721xEnumUpgradeable.sol";

contract TestNFTEnumUps is ERC721xEnumUpgradeable {

	function initialize(string memory name_, string memory symbol_) public initializer {
		__ERC721xEnum_init(name_, symbol_);
	}

	function mint(uint256 _id) external {
		_mint(msg.sender, _id);
	}

	function mint(address _user, uint256 _id) external {
		_mint(_user, _id);
	}
}