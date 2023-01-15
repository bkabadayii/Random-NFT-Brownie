from brownie import accounts, network, config, VRFCoordinatorV2Mock, AdvancedCollectible
import pytest
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
)

from scripts.deploy_and_create import (
    deploy_advanced_collectible,
    create_advanced_collectible,
)


def test_can_deploy_and_create():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")

    random_num = 67
    advanced_collectible = deploy_advanced_collectible()
    create_tx = create_advanced_collectible()
    request_id = create_tx.events["requestedCollectible"]["requestId"]
    get_contract("vrf_coordinator").fulfillRandomWordsWithOverride(
        request_id, advanced_collectible, [random_num]
    )
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_num % 3
