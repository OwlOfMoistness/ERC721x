import pytest

@pytest.fixture(scope="module")
def minter_(accounts):
    return accounts[0]

@pytest.fixture(scope="module")
def nft_lock(TestNFT, minter_):
    return TestNFT.deploy({'from':minter_})
