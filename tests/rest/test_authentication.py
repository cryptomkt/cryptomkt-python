
import json
import unittest

from cryptomarket.client import Client

with open('/home/ismael/cryptomarket/keys.json') as fd:
    keys = json.load(fd)


class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(keys['apiKey'], keys['apiSecret'])

    def tearDown(self):
        self.client.close()

    def test_authed_method(self):
        fee = self.client.get_estimate_withdrawal_fee(
            currency="XLM", amount="199")
        if fee == "":
            self.fail("no fee")


if __name__ == '__main__':
    unittest.main()
