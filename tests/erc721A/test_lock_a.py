from brownie import reverts

def test_minting(nft_lock_a, minter_, accounts):
	nft_lock_a.mint(5, {'from':accounts[1]})
	assert nft_lock_a.balanceOf(accounts[1]) == 5

def test_locking(nft_lock_a, minter_, accounts):
	nft_lock_a.updateApprovedContracts([accounts[2]], [True], {'from':minter_})
	with reverts('Cannot update map'):
		nft_lock_a.lockId(1, {'from':accounts[0]})
	nft_lock_a.lockId(1, {'from':accounts[2]})
	with reverts('ID already locked by caller'):
		nft_lock_a.lockId(1, {'from':accounts[2]})
	with reverts('Token is locked'):
		nft_lock_a.safeTransferFrom(accounts[1], accounts[4], 1, {'from':accounts[1]})

def test_unlocking(nft_lock_a, minter_, accounts):
	with reverts('Cannot update map'):
		nft_lock_a.unlockId(1, {'from':accounts[0]})
	nft_lock_a.unlockId(1, {'from':accounts[2]})
	with reverts('ID not locked by caller'):
		nft_lock_a.unlockId(1, {'from':accounts[2]})
	nft_lock_a.safeTransferFrom(accounts[1], accounts[4], 1, {'from':accounts[1]})

def test_multi_locking(nft_lock_a, minter_, accounts):
	nft_lock_a.updateApprovedContracts([accounts[3], accounts[4]], [True, True], {'from':minter_})
	nft_lock_a.lockId(2, {'from':accounts[2]})
	nft_lock_a.lockId(2, {'from':accounts[3]})
	nft_lock_a.lockId(2, {'from':accounts[4]})
	assert nft_lock_a.lockCount(2) == 3
	with reverts('Token is locked'):
		nft_lock_a.safeTransferFrom(accounts[1], accounts[4], 2, {'from':accounts[1]})
	nft_lock_a.unlockId(2, {'from':accounts[2]})
	nft_lock_a.unlockId(2, {'from':accounts[3]})
	with reverts('Token is locked'):
		nft_lock_a.safeTransferFrom(accounts[1], accounts[4], 2, {'from':accounts[1]})
	nft_lock_a.unlockId(2, {'from':accounts[4]})
	nft_lock_a.safeTransferFrom(accounts[1], accounts[4], 2, {'from':accounts[1]})

def test_free(nft_lock_a, minter_, accounts):
	nft_lock_a.lockId(2, {'from':accounts[2]})
	nft_lock_a.lockId(2, {'from':accounts[3]})
	nft_lock_a.lockId(2, {'from':accounts[4]})
	nft_lock_a.updateApprovedContracts([accounts[3], accounts[4]], [False, False], {'from':minter_})
	with reverts('Cannot update map'):
		nft_lock_a.unlockId(2, {'from':accounts[3]})
	nft_lock_a.freeId(2, accounts[3])
	nft_lock_a.freeId(2, accounts[4])
	assert nft_lock_a.lockCount(2) == 1
	nft_lock_a.unlockId(2, {'from':accounts[2]})
	assert nft_lock_a.lockCount(2) == 0