import json
import time
import unittest

from cryptomarket.client import Client
from cryptomarket.websockets import WalletClient
from tests.rest.test_helpers import good_transaction

from test_helpers import *

minute = 60
second = 1

with open('/home/ismael/cryptomarket/keys-v3.json') as fd:
    keys = json.load(fd)


class TestWSWalletClientSubs(unittest.TestCase):

    def setUp(self):
        self.ws = WalletClient(
            keys['apiKey'], keys['apiSecret'], on_error=lambda err: print(err))
        self.ws.connect()
        Veredict.reset()

    def tearDown(self):
        self.ws.close()
        time.sleep(2 * second)

    def test_subscribe_to_transactions(self):
        def callback(feed):
            if not good_transaction(feed):
                Veredict.fail('not a good transaction')
                return

        def result_callback(err, result):
            if err:
                Veredict.fail(f'err:{err}')
                return
            if not result:
                Veredict.fail('failed unsubscription')

        self.ws.subscribe_to_transactions(callback, result_callback)
        restClient = Client(keys["apiKey"], keys["apiSecret"])
        time.sleep(1 * second)
        restClient.transfer_between_wallet_and_exchange(
            currency="EOS",
            amount="0.1",
            source='spot',
            destination='wallet',
        )
        time.sleep(1 * second)
        restClient.transfer_between_wallet_and_exchange(
            currency="EOS",
            amount="0.1",
            source='wallet',
            destination='spot',
        )
        time.sleep(5 * second)
        self.ws.unsubscribe_to_transactions(result_callback)
        time.sleep(2 * second)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_balance(self):
        def callback(feed, feed_type):
            if not good_balances(feed):
                Veredict.fail('not good balances')
                return

        def result_callback(err, result):
            if err:
                Veredict.fail(f'err:{err}')
                return
            if not result:
                Veredict.fail('failed unsubscription')

        self.ws.subscribe_to_wallet_balance(callback, result_callback)
        time.sleep(3)
        self.ws.unsubscribe_to_wallet_balance(result_callback)
        time.sleep(3)
        if Veredict.failed:
            self.fail(Veredict.message)


if __name__ == '__main__':
    unittest.main()
