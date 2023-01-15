from web3 import Web3
from brownie import AdvancedCollectible, network, config, accounts, VRFCoordinatorV2Mock
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    vrf_create_sub,
    vrf_fund_sub,
    get_contract,
)

FUND_AMOUNT = Web3.toWei(1, "ether")


def deploy_advanced_collectible():
    account = get_account()

    # Get VRFCoordinator:
    vrf_keyhash = config["networks"][network.show_active()]["vrf_keyhash"]
    vrf_coordinator = get_contract("vrf_coordinator")

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        vrf_subscription_id = vrf_create_sub(vrf_coordinator)
        vrf_fund_sub(vrf_coordinator, vrf_subscription_id, FUND_AMOUNT)

    else:
        vrf_subscription_id = config["networks"][network.show_active()][
            "vrf_subscription_id"
        ]

    print("Deploying AdvancedCollectible...")
    advanced_collectible = AdvancedCollectible.deploy(
        vrf_coordinator, vrf_keyhash, vrf_subscription_id, {"from": account}
    )

    # Add consumer to vrf coordinator with sub id:
    add_consumer_tx = vrf_coordinator.addConsumer(
        vrf_subscription_id, advanced_collectible, {"from": account}
    )
    add_consumer_tx.wait(1)

    print("AdvancedCollectible deployed successfully")
    return advanced_collectible


def create_advanced_collectible(random_num=0):
    print("Creating AdvancedCollectible token...")
    advanced_collectible = AdvancedCollectible[-1]
    account = get_account()
    create_tx = advanced_collectible.createCollectible({"from": account})

    # If you are in local blockchain environment verify vrf request manually:
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        request_id = create_tx.events["requestedCollectible"]["requestId"]
        get_contract("vrf_coordinator").fulfillRandomWordsWithOverride(
            request_id, advanced_collectible, [random_num]
        )

    print("New AdvancedCollectible token created successfully!")
    return create_tx


def main():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploy_advanced_collectible()

    create_advanced_collectible()
