// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

interface ILockERC721 is IERC721 {
	function lockId(uint256 _id) external;
	function unlockId(uint256 _id) external;
	function freeId(uint256 _id, address _contract) external;
}