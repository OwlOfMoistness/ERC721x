import brownie
import pytest

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_sender_balance_decreases(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})
    balance = nft_lock_up.balanceOf(accounts[2])

    nft_lock_up.transferFrom(accounts[2], accounts[3], 1337, {'from': accounts[2]})

    assert nft_lock_up.balanceOf(accounts[2]) == balance - 1


def test_receiver_balance_increases(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})
    balance = nft_lock_up.balanceOf(accounts[3])

    nft_lock_up.transferFrom(accounts[2], accounts[3], 1337, {'from': accounts[2]})

    assert nft_lock_up.balanceOf(accounts[3]) == balance + 1


def test_caller_balance_unaffected(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})
    balance = nft_lock_up.balanceOf(accounts[4])

    nft_lock_up.approve(accounts[4], 1337, {'from': accounts[2]})
    nft_lock_up.transferFrom(accounts[2], accounts[3], 1337, {'from': accounts[4]})

    assert nft_lock_up.balanceOf(accounts[4]) == balance


def test_ownership_changes(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})
    owner = nft_lock_up.ownerOf(1337)

    nft_lock_up.transferFrom(accounts[2], accounts[3], 1337, {'from': accounts[2]})

    assert nft_lock_up.ownerOf(1337) != owner


# def test_total_supply_not_affected(nft_lock_up, accounts):
#     nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})
#     total_supply = nft_lock_up.totalSupply()

#     nft_lock_up.transferFrom(accounts[2], accounts[3], 1337, {'from': accounts[2]})

#     assert nft_lock_up.totalSupply() == total_supply


def test_safe_transfer_from_approval(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    nft_lock_up.approve(accounts[4], 1337, {'from': accounts[0]})
    nft_lock_up.safeTransferFrom(accounts[0], accounts[4], 1337, {'from': accounts[4]})
    assert nft_lock_up.ownerOf(1337) == accounts[4]


def test_safe_transfer_from_operator(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    nft_lock_up.setApprovalForAll(accounts[4], True, {'from': accounts[0]})
    nft_lock_up.safeTransferFrom(accounts[0], accounts[2], 1337, {'from': accounts[4]})
    assert nft_lock_up.ownerOf(1337) == accounts[2]


def test_transfer_no_approval(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    with brownie.reverts("ERC721: caller is not token owner or approved"):
        nft_lock_up.transferFrom(accounts[0], accounts[1], 1337, {'from': accounts[4]})


def test_safe_transfer_nonexisting(nft_lock_up, accounts):
    with brownie.reverts("ERC721: invalid token ID"):
        nft_lock_up.safeTransferFrom(accounts[0], accounts[1], 1337, {'from': accounts[0]})


def test_safe_transfer_to_zero_address(nft_lock_up, accounts, zero_addr):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    with brownie.reverts("ERC721: transfer to the zero address"):
        nft_lock_up.safeTransferFrom(accounts[0], zero_addr, 1337, {'from': accounts[0]})


def test_safe_transfer_unowned(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    nft_lock_up.approve(accounts[1], 1337, {'from': accounts[0]})
    with brownie.reverts("ERC721: transfer from incorrect owner"):
        nft_lock_up.safeTransferFrom(accounts[1], accounts[4], 1337, {'from': accounts[1]})


def test_safe_transfer_from_no_approval(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    with brownie.reverts("ERC721: caller is not token owner or approved"):
        nft_lock_up.safeTransferFrom(accounts[0], accounts[1], 1337, {'from': accounts[4]})


def test_safe_transfer_invalid_receiver(nft_lock_up, accounts, receiver_invalid):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
        nft_lock_up.safeTransferFrom(accounts[0], receiver_invalid.address, 1337, {'from': accounts[0]})


def test_transfer_invalid_receiver(nft_lock_up, accounts, receiver_invalid):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    nft_lock_up.transferFrom(accounts[0], receiver_invalid, 1337, {'from': accounts[0]})


def test_safe_transfer_invalid_receiver_return(nft_lock_up, accounts, receiver_invalid_return):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
        nft_lock_up.safeTransferFrom(accounts[0], receiver_invalid_return.address, 1337, {'from': accounts[0]})


def test_safe_transfer_valid_receiver(nft_lock_up, accounts, receiver_valid):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    nft_lock_up.safeTransferFrom(accounts[0], receiver_valid.address, 1337, {'from': accounts[0]})