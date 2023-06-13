import brownie
import pytest

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_approve(nft_lock_up, accounts, zero_addr):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})

    assert nft_lock_up.getApproved(1337) == zero_addr
    nft_lock_up.approve(accounts[1], 1337, {'from': accounts[2]})
    assert nft_lock_up.getApproved(1337) == accounts[1]


def test_change_approve(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})

    nft_lock_up.approve(accounts[1], 1337, {'from': accounts[2]})
    nft_lock_up.approve(accounts[0], 1337, {'from': accounts[2]})
    assert nft_lock_up.getApproved(1337) == accounts[0]


def test_revoke_approve(nft_lock_up, accounts, zero_addr):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})

    nft_lock_up.approve(accounts[1], 1337, {'from': accounts[2]})
    nft_lock_up.approve(zero_addr, 1337, {'from': accounts[2]})
    assert nft_lock_up.getApproved(1337) == zero_addr


def test_no_return_value(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})

    tx = nft_lock_up.approve(accounts[1], 1337, {'from': accounts[2]})
    assert tx.return_value is None


def test_approval_event_fire(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[2], 1337, {'from':accounts[0]})
    tx = nft_lock_up.approve(accounts[1], 1337, {'from': accounts[2]})
    assert len(tx.events) == 1
    assert tx.events["Approval"].values() == [accounts[2], accounts[1], 1337]


def test_illegal_approval(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    with brownie.reverts("ERC721: approve caller is not owner nor approved for all"):
        nft_lock_up.approve(accounts[1], 1337, {'from': accounts[1]})


def test_get_approved_nonexistent(nft_lock_up, accounts):
    with brownie.reverts("ERC721: approved query for nonexistent token"):
        nft_lock_up.getApproved(1337)

def test_approve_all(nft_lock_up, accounts):
    assert nft_lock_up.isApprovedForAll(accounts[0], accounts[1]) is False
    nft_lock_up.setApprovalForAll(accounts[1], True, {'from': accounts[0]})
    assert nft_lock_up.isApprovedForAll(accounts[0], accounts[1]) is True


def test_approve_all_multiple(nft_lock_up, accounts):
    operators = accounts[4:8]
    for op in operators:
        assert nft_lock_up.isApprovedForAll(accounts[1], op) is False

    for op in operators:
        nft_lock_up.setApprovalForAll(op, True, {'from': accounts[1]})

    for op in operators:
        assert nft_lock_up.isApprovedForAll(accounts[1], op) is True


def test_revoke_operator(nft_lock_up, accounts):
    nft_lock_up.setApprovalForAll(accounts[1], True, {'from': accounts[0]})
    assert nft_lock_up.isApprovedForAll(accounts[0], accounts[1]) is True

    nft_lock_up.setApprovalForAll(accounts[1], False, {'from': accounts[0]})
    assert nft_lock_up.isApprovedForAll(accounts[0], accounts[1]) is False


def test_no_return_value(nft_lock_up, accounts):
    tx = nft_lock_up.setApprovalForAll(accounts[1], True, {'from': accounts[0]})
    assert tx.return_value is None


def test_approval_all_event_fire(nft_lock_up, accounts):
    tx = nft_lock_up.setApprovalForAll(accounts[1], True, {'from': accounts[0]})
    assert len(tx.events) == 1
    assert tx.events["ApprovalForAll"].values() == [accounts[0], accounts[1], True]


def test_operator_approval(nft_lock_up, accounts):
    nft_lock_up.mint(accounts[0], 1337, {'from':accounts[0]})
    nft_lock_up.setApprovalForAll(accounts[1], True, {'from': accounts[0]})
    nft_lock_up.approve(accounts[2], 1337, {'from': accounts[1]})