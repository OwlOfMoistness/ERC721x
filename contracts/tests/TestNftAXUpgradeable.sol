// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "../erc721A/ERC721AxUpgradeable.sol";

contract TestNFTAXUps is ERC721AxUpgradeable {

	function initialize(string memory name_, string memory symbol_) public initializer initializerERC721A{
		__ERC721Ax_init(name_, symbol_);
	}

	function mint(uint256 _id) external {
		_mint(msg.sender, _id);
	}

	function mint(address _user, uint256 _id) external {
		_mint(_user, _id);
	}
}