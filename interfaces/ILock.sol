pragma solidity ^0.8.2;

interface ILock {
	function lockId(uint256 _id) external;

	function unlockId(uint256 _id) external;

	function freeId(uint256 _id, address _contract) external;
}