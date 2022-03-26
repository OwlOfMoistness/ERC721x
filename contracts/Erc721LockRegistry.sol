pragma solidity ^0.8.2;

/*
 *     ,_,
 *    (',')
 *    {/"\}
 *    -"-"-
 */

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./LockRegistry.sol";

contract Erc721LockRegistry is ERC721, LockRegistry {

	constructor(string memory _name, string memory _symbol) ERC721(_name, _symbol) {
	}

    function mint(uint256 _id) external {
        _mint(msg.sender, _id);
    }

    function transferFrom(address from, address to, uint256 tokenId) public override {
        require(isUnlocked(tokenId), "Token is locked");
		ERC721.transferFrom(from, to, tokenId);
	}

	function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory _data) public override {
        require(isUnlocked(tokenId), "Token is locked");
		ERC721.safeTransferFrom(from, to, tokenId, _data);
	}

    function lockId(uint256 _id) external  {
        require(_exists(_id), "Token !exist");
        _lockId(_id);
	}

	function unlockId(uint256 _id) external  {
        require(_exists(_id), "Token !exist");
        _unlockId(_id);
	}

	function freeId(uint256 _id, address _contract) external  {
        require(_exists(_id), "Token !exist");
        _freeId(_id, _contract);
	}
}