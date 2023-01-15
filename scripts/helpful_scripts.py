from brownie import accounts, network, config, VRFCoordinatorV2Mock, Contract
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "mainnet-fork",
    "mainnet-fork-dev",
    "development",
    "ganache-local",
]

contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorV2Mock,
}

breed_id_to_breed = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}

OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"


def get_breed(breed_id):
    return breed_id_to_breed[breed_id]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    account = get_account()

    # Deploy VRFCoordinatorV2Mock:
    print("Deploying VRFCoordinatorV2Mock...")
    VRFCoordinatorV2Mock.deploy(25000000000000000, 1000000000000, {"from": account})

    # All done!
    print("Mocks have been deployed succesfully!")


def vrf_create_sub(vrf_coordinator):
    account = get_account()
    # Create subscription:
    print("Creating new subscription...")
    sub_id_tx = vrf_coordinator.createSubscription({"from": account})
    sub_id_tx.wait(1)
    vrf_subscription_id = sub_id_tx.events["SubscriptionCreated"]["subId"]
    print(f"New subscription created successfully with subId: {vrf_subscription_id}")
    return vrf_subscription_id


def vrf_fund_sub(vrf_coordinator, sub_id, fund_amount):
    account = get_account()
    # Fund contract with Link:
    fund_amount_str = Web3.fromWei(fund_amount, "ether")
    print(f"Funding subId: {sub_id} {fund_amount_str} link tokens...")
    fund_tx = vrf_coordinator.fundSubscription(sub_id, fund_amount, {"from": account})
    fund_tx.wait(1)
    print(f"SubId: {sub_id} has been funded successfully!")


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config,
    if not defined: it will deploy a mock contract and return it.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:  # Check if a mock is deployed before
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract
