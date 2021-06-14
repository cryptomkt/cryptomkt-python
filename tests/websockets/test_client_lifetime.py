import json
import time
import unittest

import cryptomarket.args as args

from test_helpers import *

from cryptomarket.exceptions import CryptomarketSDKException
from cryptomarket.websockets import PublicClient, TradingClient, AccountClient

class TestWSPublicClient(unittest.TestCase):

    def test_public_client_lifetime(self):
        
        client = PublicClient(
            on_close= lambda: print("closing"),
            on_error= lambda err: print("error: "+err),
            on_connect = lambda: print("connected")
        )
        client.connect()
        time.sleep(5)


        client.close()
        time.sleep(3)
        
    

if __name__ == '__main__':
    unittest.main()