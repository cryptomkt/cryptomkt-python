import json
import time
import unittest
import datetime

import cryptomarket.args as args

from test_helpers import *

from cryptomarket.websockets import AccountClient

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
    
    def test_get_account_balance(self):
        def callback(err, result):
            self.assertTrue(len(result) != 0, "no balances")
            self.assertTrue(good_balances(result), "not good balances")
        self.ws.get_account_balance(callback)


    def test_load_transactions(self):
        def callback(err, result):
            self.assertTrue(len(result) != 0, "no balances")
            for transaction in result:
                self.assertTrue(good_transaction(transaction), "not good transaction")
        
        self.ws.load_transactions(callback)
        time.sleep(3 * second)

    def test_find_transactions(self):
        def callback(err, result):
            self.assertTrue(len(result) == 3, "no balances")
            for transaction in result:
                self.assertTrue(good_transaction(transaction), "not good transaction")
        
        self.ws.find_transactions(callback, limit=3)
        time.sleep(3 * second)
        
if __name__ == '__main__':
    unittest.main()