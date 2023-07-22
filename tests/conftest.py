import pytest
from brownie import Contract

@pytest.fixture(scope="module")
def zero_addr():
    return "0x0000000000000000000000000000000000000000"

@pytest.fixture(scope="module")
def minter_(accounts):
    return accounts[0]

@pytest.fixture(scope="module")
def admin(accounts):
    return accounts[10]

@pytest.fixture(scope="module")
def nft_lock(TestNFT, minter_):
    return TestNFT.deploy({'from':minter_})


@pytest.fixture(scope="module")
def nft_lock_up(TestNFTUps, MockProxy, minter_, admin):
    imp =  TestNFTUps.deploy({'from':minter_})
    data = imp.initialize.encode_input('Test', 'TEST')
    proxy = MockProxy.deploy(imp.address, admin, data, {'from': minter_})
    return Contract.from_abi("TestNFTUps", proxy.address, TestNFTUps.abi)

@pytest.fixture(scope="module")
def nft_lock_enum(TestNFTEnum, minter_):
    return TestNFTEnum.deploy({'from':minter_})


@pytest.fixture(scope="module")
def nft_lock_enum_up(TestNFTEnumUps, MockProxy, minter_, admin):
    imp =  TestNFTEnumUps.deploy({'from':minter_})
    data = imp.initialize.encode_input('Test', 'TEST')
    proxy = MockProxy.deploy(imp.address, admin, data, {'from': minter_})
    return Contract.from_abi("TestNFTUps", proxy.address, TestNFTEnumUps.abi)


@pytest.fixture(scope="module")
def nft_lock_a(TestNFTAX, minter_):
    return TestNFTAX.deploy({'from':minter_})


@pytest.fixture(scope="module")
def nft_lock_up_a(TestNFTAXUps, MockProxy, minter_, admin):
    imp =  TestNFTAXUps.deploy({'from':minter_})
    data = imp.initialize.encode_input('Test', 'TEST')
    proxy = MockProxy.deploy(imp.address, admin, data, {'from': minter_})
    return Contract.from_abi("TestNFTUps", proxy.address, TestNFTAXUps.abi)


@pytest.fixture(scope="module")
def receiver_invalid(Invalid, accounts):
	return Invalid.deploy({'from': accounts[0]})

@pytest.fixture(scope="module")
def receiver_invalid_return(InvalidReturn, accounts):
    return InvalidReturn.deploy({'from': accounts[0]})

@pytest.fixture(scope="module")
def receiver_valid(Valid, accounts):
    return Valid.deploy({'from': accounts[0]})
