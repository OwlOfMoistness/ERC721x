import pytest

@pytest.fixture(scope="module")
def minter_(accounts):
    return accounts[0]

@pytest.fixture(scope="module")
def nft_lock(Erc721LockRegistry, minter_):
    return Erc721LockRegistry.deploy('', '', {'from':minter_})

@pytest.fixture(scope="module")
def ksm(KongSafetyModule, vx_poly, minter_):
    return KongSafetyModule.deploy(vx_poly, {'from':minter_})
