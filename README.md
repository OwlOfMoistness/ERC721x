# <ins>**ERC721LockRegistry Contract**</ins>

This standard allows contract that implement the `ILock` interface to lock/unlock assets in place to enable/disable them from being transferred.

## <ins>How does this work?</ins>

The Lock Registry contains four mappings:

	mapping(address => bool) public approvedContract;
	mapping(uint256 => uint256) public lockCount;
	mapping(uint256 => mapping(uint256 => address)) public lockMap;
	mapping(uint256 => mapping(address => uint256)) public lockMapIndex;

The first, `approvedContract`, is a mapping that checks if an address is allowed to lock/unlock assets from the collection. This mapping is updated by the owner of the contract (EOA or multisig for example).

`lockCount` is a mapping that tracks how many locks a token possesses. As long as the lock count is > 0, the token cannot move. Once there are no more locks, the token is free to move once again.

`lockMap` and `lockMapIndex` work together.

`lockMap` is a double mapping that connects a token ID to the address that locked it. 

`lockMap[tokenId][lockIndex]` => contract that locked


`lockMapIndex` is a double mapping that connects a token ID to the lockIndex of the adddress that locked it.

`lockMapIndex[tokenId][lockingContract]` => lock Index of locking contract

Those 2 mappings are necessary to easily track and delete lock when a contract unlocks a token.

## <ins>Interface</ins>

The `ILock` interface is very simple:

	interface ILock {
		function lockId(uint256 _id) external;
		function unlockId(uint256 _id) external;
		function freeId(uint256 _id, address _contract) external;
	}

The first 2 functions are self explanatory. An approved contract can lock or unlock an asset. Locking an asset twice will revert, same behaviour for double unlocking.

`freeId` is an emergency function that can only be called under specific condition. Under the hood, it behaves similarly to the `unlockId` function. It can only be called if the previously approved contract that locked the asset is not approved anymore. This means that `approvedContract[badContract] => false` will be required and can be changed by calling `updateApprovedContracts` and unset the initially approved contract. This should happen if the locking contract has bad logic and prevents people from unlocking assets. By disapproving the defective contract, we allow users to remove the lock to enable transferring their asset if they choose to.


## <ins>What can it do?</ins>

The lock registry is very powerful. It allows to lock assets in place which is the underlying condition of staking or securing assets.
This means that the lock registry is ideal to guarantee that assets cannot be transferred in staking mechanisms.
A good example would be the [Play and Kollect experience created by CyberKongz](https://docs.cyberkongz.com/).

When locking an asset, the token does not need to move to a contract to interact with it and therefore does not have to leave the owner's wallet. In addition to reducing contract risks, asset holders are thus given the option to engage in an unlimited number of previously approved locking contracts simultaneously, while always retaining actual ownership of the asset.

Furthermore it can be used to secure assets. If assets cannot move, that means that they can't be stolen. This makes the possibility to create onchain 2fa, so to speak.
Assets could reside on a hot wallet (metamask) but be secured by a guardian address that is a multisig or a HW wallet. This allows to benefit from the flexibility of hot wallet interactions on metamask while keeping the high security of using HW wallets or multisigs without needing to click/sign endlessly your devices. [A twitter experiment by Owl has been done on twitter](https://twitter.com/OwlOfMoistness/status/1504203389915308048).
