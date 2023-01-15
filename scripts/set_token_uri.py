from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_breed,
    OPENSEA_URL,
)
from scripts.deploy_and_create import (
    deploy_advanced_collectible,
    create_advanced_collectible,
)

nft_meta_data_dict = {
    "PUG": "https://ipfs.io/ipfs/QmdUhcZWh8bRPjXYJaBnYvbhRNTGiMvRafFwi7sTbePaGT?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmT2NPZchxsV3rNYxLswxthj13YwK3tW4HcKjpJCZA8Mo4?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmVForFc29hQCX6GwBMBa4N1oH72gUdTo9R4yYb8bvnKEJ?filename=2-ST_BERNARD.json",
}


def set_token_uri(token_id, token_uri, nft_contract):
    account = get_account()
    set_token_uri_tx = nft_contract.setTokenURI(token_id, token_uri, {"from": account})
    set_token_uri_tx.wait(1)
    print(f"Token URI for token id: {token_id} has been set!")
    print(
        f"You can view your NFT at: {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )


def main():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploy_advanced_collectible()
        create_advanced_collectible(0)
        create_advanced_collectible(1)
        create_advanced_collectible(2)

    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    number_of_collectibles = 2
    print(f"You have {number_of_collectibles} tokens!")
    for token_id in range(number_of_collectibles):
        breed_id = advanced_collectible.tokenIdToBreed(token_id)
        breed = get_breed(breed_id)

        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            set_token_uri(token_id, nft_meta_data_dict[breed], advanced_collectible)
