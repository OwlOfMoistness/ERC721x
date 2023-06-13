pragma solidity ^0.8.11;

contract InvalidReturn {
	function onERC721Received(address _operator, address _from, uint256 _tokenId, bytes memory _data) 
		external returns(bytes4) {
		return 0x0;
	}
}