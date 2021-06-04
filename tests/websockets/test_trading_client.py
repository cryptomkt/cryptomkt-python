import json
import time
import unittest

import cryptomkt.args as args

from test_helpers import *

from cryptomarket.exceptions import CryptomarketSDKException
from cryptomarket.websockets import TradingClient


with open('/home/ismael/cryptomarket/apis/keys.json') as fd:
    keys = json.load(fd)

class TestWSTradingClient(unittest.TestCase):

    def setUp(self):
        self.ws = TradingClient(keys['apiKey'], keys['apiSecret'],on_error=lambda err: print(err))
        self.ws.connect()
    
    def tearDown(self):
        self.ws.close()
    
    def test_create_get_and_cancel_order(self):
        client_order_id = str(int(time.time()))
        def on_active_orders(err, order_list):
            self.assertIsNone(err,"error in request: " + str(err))
            self.assertTrue(good_order_list(order_list),"not good orders")
            for order in order_list:
                self.assertTrue(order['clientOrderId'] != client_order_id+"new",'order not canceled')

        def on_canceled_order(err, canceled_order):
            self.assertIsNone(err,"error in request: " + str(err))
            self.assertTrue(canceled_order['reportType'] == 'canceled', "should be canceled")
            self.assertTrue(good_order(canceled_order),"not good order")
            
            self.ws.get_active_orders(on_active_orders)


        def on_replaced_order(err, order_replaced):
            self.assertIsNone(err,"error in request: " + str(err))
            self.assertTrue(good_order(order_replaced), "not good order")
            self.assertTrue(order_replaced['reportType']== 'replaced', "should be replaced")

            client_order_id = order_replaced['clientOrderId']
            self.ws.cancel_order(client_order_id, on_canceled_order)

        def on_order_created(err, new_order):
            self.assertIsNone(err,"error in request: " + str(err))
            self.assertTrue(good_order(new_order), "not good order")
            self.assertTrue(new_order['status']=='new', "should be new")
            self.ws.replace_order(
                client_order_id,
                client_order_id+"new",
                '0.01',
                '101010',
                callback=on_replaced_order,
            )

        self.ws.create_order(
            client_order_id,
            'EOSETH',
            'sell',
            '0.01',
            price='10000',
            callback=on_order_created)
        time.sleep(7)

    def test_get_trading_balance(self):
        def check_good_balances(err, balances):
            self.assertTrue(err is None,"error in request: " + str(err))
            self.assertTrue(len(balances)>0, "no balances")
            self.assertTrue(good_balances(balances), "not good balances")
        self.ws.get_trading_balance(check_good_balances)
        time.sleep(3)


if __name__ == '__main__':
    unittest.main()