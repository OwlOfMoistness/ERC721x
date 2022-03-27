**ERC721LockRegistry Contract**

This standard allows contract that implement the ILock interface to lock/unlock assets in place to enable/disable them from being transferred.

How does this work?

The Lock Registry contain four mappings:

	mapping(address => bool) public approvedContract;
	mapping(uint256 => uint256) public lockCount;
	mapping(uint256 => mapping(uint256 => address)) public lockMap;
	mapping(uint256 => mapping(address => uint256)) public lockMapIndex;

The first, approvedContract, is a mapping that checks if an address is allowed to lock/unlock assets from the collection. This mapping is updated by the owner of the contract (EOA or multisig for example).

lockCount is a mapping that tracks how many locks a token possesses. As long as the lock count is > 0, the token cannot move. Once there are no more locks, the token is free to move once again.

lockMap and lockMap Index work together.
lockMap is a double mapping that connects a token ID to the address that locked it. 
lockMap[tokenId][lockIndex] => contract that locked
lockMapIndex is a double mapping that connects a token ID to the lockIndex of the adddress that locked it.
lockMapIndex[tokenId][lockingContract] => lock Index of locking contract

Those 2 mappings are necessary to easily track and delete lock when a contract unlocks a token


The ILock interace is very simple:

interface ILock {
	function lockId(uint256 _id) external;
	function unlockId(uint256 _id) external;
	function freeId(uint256 _id, address _contract) external;
}

The first 2 functions are self explanatory. An approved contract can lock or unlock an asset. Locking at an asset twice will revert, same behaviour for double unlocking.

freeId is an emergency function that can only be called under specific condition. Under the hood, it behaves similarly to the unlockId function. It can only be called if the previously approved contract that locked the asset is not approved anymore. This will happen if the locking contract has bad logic and prevents people from unlocking assets. By disapproving the defective contract, we allow users to remove the lock to enable transferring their asset if the choose to.