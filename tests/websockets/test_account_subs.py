import json
import time
import unittest
import datetime


from test_helpers import *

from cryptomarket.websockets import AccountClient, TradingClient
from cryptomarket.client import Client
import cryptomarket.args as args

minute = 60
second = 1

with open('/home/ismael/cryptomarket/apis/keys.json') as fd:
    keys = json.load(fd)

class TestWSClientTradingSubs(unittest.TestCase):

    def setUp(self):
        self.ws = AccountClient(keys['apiKey'], keys['apiSecret'], on_error=lambda err: print(err))
        self.ws.connect()
    
    def tearDown(self):
        self.ws.close()
        time.sleep(2 * second)
    
    def test_subscribe_transactions(self):
        def callback(feed):
            print(feed)
            self.assertTrue(good_transaction(feed), "not good transaction")

        self.ws.subscribe_to_transactions(callback)
        restClient = Client(keys["apiKey"], keys["apiSecret"])
        time.sleep(1 * second)
        restClient.transfer_money_from_bank_balance_to_trading_balance("EOS", "0.1")
        time.sleep(1 * second)
        restClient.transfer_money_from_trading_balance_to_bank_balance("EOS", "0.1")
        time.sleep(5 * second)
        self.ws.unsubscribe_to_transactions()
        time.sleep(2 * second)
    
    def test_subscribe_balance(self):
        def callback(feed):
            print(feed)
            self.assertTrue(good_balances(feed), 'not good balances')
        
        self.ws.subscribe_to_balance(callback)
        time.sleep(3)
        

        
if __name__ == '__main__':
    unittest.main()