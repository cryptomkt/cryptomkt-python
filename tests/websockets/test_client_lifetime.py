import time
import unittest

from test_helpers import *

from cryptomarket.websockets import MarketDataClient


class TestWSPublicClient(unittest.TestCase):

    def test_public_client_lifetime(self):

        client = MarketDataClient(
            on_close=lambda: print("closing"),
            on_error=lambda err: print("error: "+err),
            on_connect=lambda: print("connected")
        )
        client.connect()
        time.sleep(5)

        client.close()
        time.sleep(3)


if __name__ == '__main__':
    unittest.main()
