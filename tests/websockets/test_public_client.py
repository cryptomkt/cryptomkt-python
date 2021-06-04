import json
import time
import unittest

import cryptomkt.args as args

from test_helpers import *

from cryptomarket.exceptions import CryptomarketSDKException
from cryptomarket.websockets import PublicClient

class TestWSPublicClient(unittest.TestCase):

    def setUp(self):
        self.ws = PublicClient(on_error=lambda err: print(err))
        self.ws.connect()
    
    def tearDown(self):
        self.ws.close()
        time.sleep(2)
        

    def test_get_currency(self):
        def check_good_currency(err, data):
            if err is not None:
                print("error in the call")
            if not good_currency(data):
                print("not good currency")
            
        self.ws.get_currency('EOS', check_good_currency)
        time.sleep(3)
    
    def test_get_currencies(self):
        def check_good_currencies(err, curr_list):
            for curr in curr_list:
                if not good_currency(curr):
                    print("not good currency")
        self.ws.get_currencies(check_good_currencies)
        time.sleep(3)

    def test_get_symbol_no_callback(self):
        with self.assertRaises(Exception):
            self.ws.get_symbol('EOSETH') # needs callback
        

    def test_get_symbol_not_exist(self):
        def fail_on_success(err, data):
            if err is None:
                print("error is none")

        self.ws.get_symbol('asymbol', fail_on_success)
        time.sleep(3)
    
    def test_get_symbols(self):
        def check_good_symbol(err, symbols):
            if err is not None: print("error in the request")
            for symbol in symbols:
                if not good_symbol(symbol):
                    print("not good symbol")
        self.ws.get_symbols(check_good_symbol)
        time.sleep(3)
    
    def test_get_trades(self):
        def check_good_trades(err, trades):
            if err is not None: print("error in the request")
            for trade in trades:
                if not good_public_trade(trade):
                    print("not good trade")
        self.ws.get_trades('EOSETH', check_good_trades, limit=2)
        time.sleep(3)

if __name__ == '__main__':
    unittest.main()