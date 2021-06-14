import json
import unittest
import time

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


class GetTradingBalance(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            trading_balance = self.client.get_trading_balance()
            if len(trading_balance) == 0: self.fail("no balances")
            if not good_balances(trading_balance):
                self.fail("not good balance")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")


class CreateOrder(AuthCallsTestCase):
    def test_create_order_default_arguments(self): # default on optional arguments, ('price' required on 'limit' orders, the default type)
        try:
            new_order = self.client.create_order(
                symbol='EOSETH',
                side='sell',
                quantity='0.01',
                price="1000",
            )
            if not good_order(new_order): self.fail("not good order")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

    def test_exception_for_selling_nothing(self):
        with self.assertRaises(CryptomarketSDKException):
            new_order = self.client.create_order(
                symbol='EOSETH',
                side='sell',
                order_type='limit',
                quantity='0',
                price="1000",
            )
    
    def test_readme_example(self):
        with self.assertRaises(CryptomarketSDKException):
            order = self.client.create_order(
                symbol='eosehtt',  # non existant symbol
                side='sell',
                quantity='10', 
            )

    def test_readme_example_2(self):
        with self.assertRaises(ArgumentFormatException):
            order = self.client.create_order(
                symbol='EOSETH', 
                side='selllll', # wrong
                quantity='3'
            )

class GetActiveOrders(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            active_orders = self.client.get_active_orders()
            if not good_order_list(active_orders): self.fail("not good orders")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

    def test_filter_by_symbol(self):
        try:
            active_orders = self.client.get_active_orders(symbol='EOSETH')
            if not good_order_list(active_orders): self.fail("not good order")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class OrderFlow(AuthCallsTestCase):
    def test_wrong_id_call(self):
        with self.assertRaises(CryptomarketSDKException):
            active_order = self.client.get_active_order(client_order_id='123')

    def test_successfull_call(self): # create order should work properly
        try:
            client_order_id= str(time.time())
            order = self.client.create_order(
                symbol='EOSETH',
                side=args.SIDE.SELL,
                quantity='0.01',
                order_type=args.ORDER_TYPE.LIMIT,
                client_order_id=client_order_id,
                price='1000')
            if not good_order(order): self.fail("not good order")
            order = self.client.get_active_order(client_order_id)
            if not good_order(order): self.fail("not good order")
            order = self.client.cancel_order(client_order_id)
            if not good_order(order): self.fail("not good order")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class CancellAllActiveOrders(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            for i in range(3):
                self.client.create_order(symbol='EOSETH',side=args.SIDE.SELL,quantity='0.01',order_type=args.ORDER_TYPE.LIMIT,price='1000')
            
            orders = self.client.get_active_orders(symbol='EOSETH')
            self.assertTrue(len(orders) >= 3, 'should have at least 3 orders')
            
            self.client.cancel_all_orders(symbol='EOSETH')

            orders_after_cancel = self.client.get_active_orders(symbol='EOSETH')
            self.assertTrue(len(orders_after_cancel) == 0, "shouldn't have orders")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")


class CancelOrderByClientId(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            order = self.client.create_order(
                symbol='EOSETH',
                side=args.SIDE.SELL,
                quantity='0.01',
                order_type=args.ORDER_TYPE.LIMIT,
                price='1000'
            )
            client_order_id = order['clientOrderId']
            response = self.client.cancel_order(client_order_id)
            if not good_order(response): self.fail("Not good order")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

        with self.assertRaises(CryptomarketSDKException):
            order = self.client.get_active_order(client_order_id)

            
class GetTradingCommission(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            trading_comssion = self.client.get_trading_commission('EOSETH')
            if trading_comssion == "": self.fail("not valid trading commision")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class CancelingOrders(AuthCallsTestCase):
    def test_cancel_all_with_arguments(self):
        try:
            self.client.cancel_all_orders()  
            order = self.client.create_order(
                symbol='EOSETH',
                side='sell', 
                quantity='0.01',
                price='1001',
            )
            order = self.client.create_order(
                symbol='EOSBTC',
                side='sell', 
                quantity='0.01',
                price='1001',
            )
            response = self.client.cancel_all_orders('EOSETH')
            if len(response) == 2: self.fail("should only cancel one order")
            self.client.cancel_all_orders()  
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")
        

if __name__ == '__main__':
    unittest.main()