// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

/*
 *     ,_,
 *    (',')
 *    {/"\}
 *    -"-"-
 */

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./LockRegistry.sol";
import "../interfaces/ILock.sol";

contract ERC721x is ERC721, LockRegistry {

	/*
     *     bytes4(keccak256('freeId(uint256,address)')) == 0x94d216d6
     *     bytes4(keccak256('isUnlocked(uint256)')) == 0x72abc8b7
     *     bytes4(keccak256('lockCount(uint256)')) == 0x650b00f6
     *     bytes4(keccak256('lockId(uint256)')) == 0x2799cde0
     *     bytes4(keccak256('lockMap(uint256,uint256)')) == 0x2cba8123
     *     bytes4(keccak256('lockMapIndex(uint256,address)')) == 0x09308e5d
     *     bytes4(keccak256('unlockId(uint256)')) == 0x40a9c8df
     *
     *     => 0x94d216d6 ^ 0x72abc8b7 ^ 0x650b00f6 ^ 0x2799cde0 ^
     *        0x2cba8123 ^ 0x09308e5d ^ 0x40a9c8df  == 0xc1c8d4d6
     */

	bytes4 private constant _INTERFACE_ID_LOCKABLE = 0xc1c8d4d6;

	constructor(string memory _name, string memory _symbol) ERC721(_name, _symbol) {
	}

    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721) returns (bool) {
        return interfaceId == _INTERFACE_ID_LOCKABLE
            || super.supportsInterface(interfaceId);
    }

	function transferFrom(address from, address to, uint256 tokenId) public override {
		require(isUnlocked(tokenId), "Token is locked");
		ERC721.transferFrom(from, to, tokenId);
	}

	function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory _data) public override {
		require(isUnlocked(tokenId), "Token is locked");
		ERC721.safeTransferFrom(from, to, tokenId, _data);
	}

	function lockId(uint256 _id) external override {
		require(_exists(_id), "Token !exist");
		_lockId(_id);
	}

	function unlockId(uint256 _id) external override {
		require(_exists(_id), "Token !exist");
		_unlockId(_id);
	}

	function freeId(uint256 _id, address _contract) external override {
		require(_exists(_id), "Token !exist");
		_freeId(_id, _contract);
	}
}