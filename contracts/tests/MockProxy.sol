pragma solidity ^0.8.17;

import"@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";


contract MockProxy is TransparentUpgradeableProxy {
	constructor(address _logic, address _admin, bytes memory _data) public  TransparentUpgradeableProxy(_logic, _admin, _data) {}
}