
import json
import unittest

from cryptomarket.client import Client
from cryptomarket.exceptions import CryptomarketSDKException


with open('/home/ismael/cryptomarket/keys-v3.json') as fd:
    keys = json.load(fd)


class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(keys['apiKey'], keys['apiSecret'])


    def tearDown(self):
        self.client.close()

    def test_authed_method(self):
        try:
            fee = self.client.get_estimate_withdrawal_fee(
                currency="XLM", amount="199")
            if fee == "":
                self.fail("no fee")
        except CryptomarketSDKException as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()


