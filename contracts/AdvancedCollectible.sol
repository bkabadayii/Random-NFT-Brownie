//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBaseV2 {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint64 public subscriptionId;
    uint32 randomWordCount;
    uint32 vrfCallbackGasLimit = 100000;
    uint16 vrfRequestConfirmations = 3;
    VRFCoordinatorV2Interface COORDINATOR;

    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(uint256 => address) requestIdToSender;

    event requestedCollectible(uint256 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        bytes32 _keyhash,
        uint64 _subscriptionId
    )
        //address _linkToken
        ERC721("Dogie", "DOG")
        VRFConsumerBaseV2(_vrfCoordinator)
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        subscriptionId = _subscriptionId;
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        randomWordCount = 1;
    }

    function fulfillRandomWords(
        uint256 requestId,
        uint256[] memory _randomWords
    ) internal override {
        Breed currentBreed = Breed(_randomWords[0] % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = currentBreed;
        emit breedAssigned(newTokenId, currentBreed);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        //_setTokenURI(newTokenId, _tokenURI);
        tokenCounter++;
    }

    function requestRandomWords() internal returns (uint256) {
        uint256 requestId = COORDINATOR.requestRandomWords(
            keyhash,
            subscriptionId,
            vrfRequestConfirmations,
            vrfCallbackGasLimit,
            randomWordCount
        );
        return requestId;
    }

    function createCollectible() public returns (uint256) {
        uint256 requestId = requestRandomWords();
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
        return requestId;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "Not approved or owner!"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
