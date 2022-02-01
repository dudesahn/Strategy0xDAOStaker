import brownie
from brownie import Contract
from brownie import config
import math


def test_base_strategy(
    gov,
    token,
    vault,
    strategist,
    whale,
    strategy,
    chain,
    amount,
    masterchef,
    pid,
):
    ## deposit to the vault after approving
    startingWhale = token.balanceOf(whale)
    token.approve(vault, 2 ** 256 - 1, {"from": whale})
    vault.deposit(amount, {"from": whale})
    newWhale = token.balanceOf(whale)

    to_view = []
    for i in range(3):
        addy = masterchef.poolInfo(i)[0]
        to_view.append(addy)
    print("These are our addresses", to_view)
    print("This is our pid", pid)
    print("This is our token symbol:", token.symbol())

    # test our harvestTrigger for when we have a profit (don't normally need this)
    # our whale donates dust to the vault, what a nice person!
    donation = amount / 10
    token.transfer(strategy, donation, {"from": whale})
    chain.sleep(86400 * 4)  # fast forward so our min delay is passed
    chain.mine(1)

    tx = strategy.harvestTrigger(0, {"from": gov})
    print("\nShould we harvest? Should be true.", tx)
    assert tx == True

    # test all of our random shit
    strategy.doHealthCheck()
    strategy.healthCheck()
    strategy.apiVersion()
    strategy.name()
    strategy.delegatedAssets()
    strategy.vault()
    strategy.strategist()
    strategy.rewards()
    strategy.keeper()
    strategy.want()
    strategy.minReportDelay()
    strategy.maxReportDelay()
    strategy.profitFactor()
    strategy.debtThreshold()
    strategy.emergencyExit()
