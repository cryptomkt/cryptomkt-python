import json
import time
import unittest
from cryptomarket.dataclasses.order import OrderStatus

from test_helpers import *

import cryptomarket.args as args
from cryptomarket.client import Client
from cryptomarket.exceptions import CryptomarketSDKException

with open('/home/ismael/cryptomarket/keys.json') as fd:
    keys = json.load(fd)


class AuthCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.apiKey = keys['apiKey']
        self.apiSecret = keys['apiSecret']
        self.client = Client(self.apiKey, self.apiSecret)

    def tearDown(self):
        self.client.close()


class ChangeCredentials(AuthCallsTestCase):
    def test_change_credentials(self):
        trading_balances = self.client.get_spot_trading_balances()
        if len(trading_balances) == 0:
            self.fail("no balances")
        if not good_list(good_balance, trading_balances):
            self.fail("not good balance")

        self.client.change_credentials("", "")
        try:
            trading_balances = self.client.get_spot_trading_balances()
            self.fail("should fail")
        except CryptomarketSDKException:
            pass

        self.client.change_credentials(self.apiKey, self.apiSecret)
        trading_balances = self.client.get_spot_trading_balances()
        if len(trading_balances) == 0:
            self.fail("no balances")
        if not good_list(good_balance, trading_balances):
            self.fail("not good balance")


if __name__ == '__main__':
    unittest.main()
