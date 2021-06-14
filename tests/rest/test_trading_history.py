import json
import unittest

import cryptomarket.args as args

from test_helpers import *

from cryptomarket.client import Client

from cryptomarket.exceptions import ArgumentFormatException
from cryptomarket.exceptions import CryptomarketSDKException



with open('/home/ismael/cryptomarket/apis/keys.json') as fd:
    keys = json.load(fd)

class AuthCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(keys['apiKey'], keys['apiSecret'])
    
    def tearDown(self):
        self.client.close()


class GetOrderHistory(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            order_history = self.client.get_orders_history('EOSETH')
            if len(order_history) == 0: self.fail("should have orders")
            if not good_order_list(order_history): self.fail("not good order")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class GetOrder(AuthCallsTestCase):
    def test_no_such_order(self):
        try:
            orders = self.client.get_orders_by_client_order_id('blah')
            if len(orders) != 0: self.fail("should not have orders")
        except:
            self.fail("should not fail")

    def test_successfull_call(self):
        try:
            orders = self.client.get_orders_by_client_order_id('99e9b6d5a6f4f575ebad8b14a7c196a8')
            if not good_order_list(orders): self.fail("not good order")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class GetTradesHistory(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            trades_history = self.client.get_trades_history('EOSETH')
            for trade in trades_history:
                if not good_trade(trade): self.fail("not good trade")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class GetTradesByOrder(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            trades = self.client.get_trades_by_order(order_id=337789478188)
            if len(trades) == 0: self.fail("no trades of order")
            for trade in trades:
                if not good_trade(trade): self.fail("not good trade")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")




if __name__ == '__main__':
    unittest.main()