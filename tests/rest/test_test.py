import json
import time
from typing import Dict, List
from cryptomarket.args import TickerSpeed
from cryptomarket.dataclasses.wsTicker import WSTicker
from cryptomarket.dataclasses.wsTrade import WSTrade
from cryptomarket.websockets.wallet_client import WalletClient


with open('/home/ismael/cryptomarket/keys.json') as fd:
    keys = json.load(fd)


def print_report(exception, report):
    if exception is not None:
        print('exception')
        print(exception)
    if report is not None:
        print('report')
        print(report)


if __name__ == '__main__':
    from cryptomarket.websockets import TradingClient

    client = WalletClient(keys['apiKey'], keys['apiSecret'], window=15_000)
    client.connect()

    # subscribe to wallet transactions
    def callback(transaction):
        print(transaction)
    client.subscribe_to_transactions(callback)

    # unsubscribe from wallet transactions
    err = client.unsubscribe_to_transactions()

    # get wallet balances
    def callback(err, balances):
        if err:
            print(err)
            return
        print(balances)
    client.get_wallet_balances(callback)

    time.sleep(5)

    client.close()
