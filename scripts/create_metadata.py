import json
from brownie import AdvancedCollectible, network, config
from scripts.helpful_scripts import get_breed, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy_and_create import (
    deploy_advanced_collectible,
    create_advanced_collectible,
)
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests


def main():
    # If you are in local blockchain, deploy contract and create token(s):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploy_advanced_collectible()
        create_advanced_collectible(0)
        create_advanced_collectible(1)
        create_advanced_collectible(2)

    advanced_collectible = AdvancedCollectible[-1]
    num_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {num_collectibles} advanced collectibles!")

    for token_id in range(num_collectibles):
        breed_id = advanced_collectible.tokenIdToBreed(token_id)
        breed = get_breed(breed_id)
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )

        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to override!")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed}"
            image_path = "img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        end_point = "/api/v0/add"
        ipfs_response = requests.post(
            ipfs_url + end_point, files={"file": image_binary}
        )
        ipfs_hash = ipfs_response.json()["Hash"]

        # Str formatting:
        filename = filepath.split("/")[-1:][0]

        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
