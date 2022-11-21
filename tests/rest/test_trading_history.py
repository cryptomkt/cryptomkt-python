import json
import unittest

from cryptomarket.client import Client
from cryptomarket.exceptions import CryptomarketSDKException

from test_helpers import *

with open('/home/ismael/cryptomarket/keys-v3.json') as fd:
    keys = json.load(fd)


class AuthCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(keys['apiKey'], keys['apiSecret'])

    def tearDown(self):
        self.client.close()


class GetOrderHistory(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            order_history = self.client.get_spot_orders_history('EOSETH')
            # if len(order_history) == 0:
            #     self.fail("should have orders")
            if not good_list(good_order, order_history):
                self.fail("not good order")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")


class GetTradesHistory(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            trades_history = self.client.get_spot_trades_history(
                symbol='EOSETH')
            if not good_list(good_trade, trades_history):
                self.fail("not good trade")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")


if __name__ == '__main__':
    unittest.main()
