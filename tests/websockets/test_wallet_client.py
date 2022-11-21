import json
import unittest

from cryptomarket.websockets import WalletClient
from tests.rest.test_helpers import good_balance, good_transaction

from test_helpers import *

with open('/home/ismael/cryptomarket/keys-v3.json') as fd:
    keys = json.load(fd)

class TestWSWalletClient(unittest.TestCase):

    def setUp(self):
        self.ws = WalletClient(
            keys['apiKey'], keys['apiSecret'], on_error=lambda err: print(err))
        self.ws.connect()
        Veredict.reset()

    def tearDown(self):
        self.ws.close()

    def test_get_wallet_balances(self):
        def check_good_balances(err, balances):
            if err is not None:
                Veredict.fail(f'{err}')
                return
            if not len(balances) > 0:
                Veredict.fail("no balances")
                return
            if not good_balances(balances):
                Veredict.fail("not good balances")
                return
            Veredict.done = True
        self.ws.get_wallet_balances(check_good_balances)
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_get_wallet_balance_of_currency(self):
        def check_good_balance(err, balance):
            if err is not None:
                Veredict.fail(f'{err}')
                return
            if not good_balance(balance):
                Veredict.fail("not good balances")
                return
            Veredict.done = True
        self.ws.get_wallet_balance_of_currency('EOS', check_good_balance)
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_get_transactions(self):
        def check_good_transactions(err, transactions):
            if err is not None:
                Veredict.fail(f'{err}')
                return
            for transaction in transactions:
                if not good_transaction(transaction):
                    Veredict.fail('not a good transaction')
                    return
            Veredict.done = True
        self.ws.get_transactions(check_good_transactions)
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)


if __name__ == '__main__':
    unittest.main()
