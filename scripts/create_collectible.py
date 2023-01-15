from brownie import AdvancedCollectible, accounts, config, network
from scripts.helpful_scripts import get_account, get_contract


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    create_tx = advanced_collectible.createCollectible({"from": account})
    create_tx.wait(1)
    print("Collectible created successfully!")
