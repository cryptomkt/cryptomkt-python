import json
import unittest

import cryptomarket.args as args
from cryptomarket.client import Client
from cryptomarket.exceptions import CryptomarketSDKException

from test_helpers import *

with open('/home/ismael/cryptomarket/keys-v3.json') as fd:
    keys = json.load(fd)


class AuthCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(keys['apiKey'], keys['apiSecret'])

    def tearDown(self):
        self.client.close()


class GetWalletBalances(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            result = self.client.get_wallet_balances()
            if len(result) == 0:
                self.fail("no balances")
            if not good_list(good_balance, result):
                self.fail("not good balances")
        except CryptomarketSDKException as e:
            self.fail(e)


class GetWalletBalanceOfCurrency(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            result = self.client.get_wallet_balance_of_currency("CRO")
            if not good_balance(result):
                self.fail("not a good balance")
        except CryptomarketSDKException as e:
            self.fail(e)


class GetDepositCryptoAddresses(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            result = self.client.get_deposit_crypto_addresses()
            if not good_list(good_address, result):
                self.fail("not a good address")
        except CryptomarketSDKException as e:
            self.fail(e)


class GetDepositCryptoAddressOfCurrency(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            result = self.client.get_deposit_crypto_address_of_currency('EOS')
            if not good_address(result):
                self.fail("not a good address")
        except CryptomarketSDKException as e:
            self.fail(e)


class CreateDepositCryptoAddress(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            result = self.client.create_deposit_crypto_address('EOS')
            if not good_address(result):
                self.fail("not a good address")
        except CryptomarketSDKException as e:
            self.fail(e)


class Last10DepositCryptoAddress(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            result = self.client.last_10_deposit_crypto_address('EOS')
            if len(result) == 0:
                self.fail("not enough addresses")
            if not good_list(good_address, result):
                self.fail("not a good address")
        except CryptomarketSDKException as e:
            self.fail(e)


class Last10WithdrawalCryptoAddress(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            result = self.client.last_10_withdrawal_crypto_address('EOS')
            if not good_list(good_address, result):
                self.fail("not a good address")
        except CryptomarketSDKException as e:
            self.fail(e)


class WithdrawCrypto(AuthCallsTestCase):
    def test_call_random_id(self):
        with self.assertRaises(CryptomarketSDKException):
            response = self.client.withdraw_crypto_commit(
                id=37176135661  # random number
            )

    def test_successfull_call(self):
        # works good
        pass
        # try:
        #     adaAddress = self.client.get_deposit_crypto_address_of_currency(
        #         "ADA")
        #     result = self.client.withdraw_crypto(
        #         currency='ADA',
        #         amount='0.1',
        #         address=adaAddress.address,
        #     )
        #     if result == "":
        #         self.fail("no transaction id")
        # except CryptomarketSDKException as e:
        #     self.fail(e)


class WithdrawCryptoCommit(AuthCallsTestCase):
    def test_successfull_call(self):
        # works good
        pass
        # try:
        #     adaAddress = self.client.get_deposit_crypto_address_of_currency(
        #         "ADA")
        #     transaction_id = self.client.withdraw_crypto(
        #         currency='ADA',
        #         amount='0.1',
        #         address=adaAddress.address,
        #         auto_commit=False
        #     )
        #     if transaction_id == "":
        #         self.fail("no transaction id")
        #     success = self.client.withdraw_crypto_commit(transaction_id)
        #     if not success:
        #         self.fail("not a successful commit")
        # except CryptomarketSDKException as e:
        #     self.fail(e)


class WithdrawCryptoRollback(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            adaAddress = self.client.get_deposit_crypto_address_of_currency(
                "ADA")
            transaction_id = self.client.withdraw_crypto(
                currency='ADA',
                amount='0.1',
                address=adaAddress.address,
                auto_commit=False
            )
            if transaction_id == "":
                self.fail("no transaction id")
            success = self.client.withdraw_crypto_rollback(transaction_id)
            if not success:
                self.fail("not a successful rollback")
        except CryptomarketSDKException as e:
            self.fail(e)


class TestGetEstimateWithdrawalFee(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            fee = self.client.get_estimate_withdrawal_fee(
                currency="XLM", amount="199")
            if fee == "":
                self.fail("no fee")
        except CryptomarketSDKException as e:
            self.fail(e)


class CryptoAddressBelongsToCurrentAccount(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            address = self.client.get_deposit_crypto_address_of_currency("ADA")
            response = self.client.check_if_crypto_address_belong_to_current_account(
                address.address
            )
            if response == False:
                self.fail('should belong')
        except CryptomarketSDKException as e:
            self.fail(e)


class TransferBetweenWalletAndExchange(AuthCallsTestCase):
    def test_successful_call(self):
        try:
            transaction_id = self.client.transfer_between_wallet_and_exchange(
                currency="ADA",
                amount="0.1",
                source=args.ACCOUNT.SPOT,
                destination=args.ACCOUNT.WALLET
            )
            if transaction_id == "":
                self.fail('no transaction id')
            transaction_id = self.client.transfer_between_wallet_and_exchange(
                currency="ADA",
                amount="0.1",
                source=args.ACCOUNT.WALLET,
                destination=args.ACCOUNT.SPOT
            )
            if transaction_id == "":
                self.fail('no transaction id')
        except CryptomarketSDKException as e:
            self.fail(e)


class TransferMoneyToAnotherUser(AuthCallsTestCase):
    def test_successful_call(self):
        pass
        # try:
        #     transaction_id = self.client.transfer_money_to_another_user(
        #         currency="CRO",
        #         amount="0.1",
        #         identify_by=args.IDENTIFY_BY.EMAIL,
        #         email="the email"
        #     )
        #     if transaction_id == "":
        #         self.fail('no transaction id')
        # except CryptomarketSDKException as e:
        #     self.fail(e)


class GetTransactionsHistory(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            result = self.client.get_transaction_history(currencies=['EOS'])
            if not good_list(good_transaction, result):
                self.fail("no good transaction")
        except CryptomarketSDKException as e:
            self.fail(e)


class GetTransaction(AuthCallsTestCase):
    def test_successfull_call(self):
        # see ruby sdk for further information
        pass


class OffchainAvailable(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            eosAddress = self.client.get_deposit_crypto_address_of_currency(
                "EOS")
            self.client.check_if_offchain_is_available(
                currency="EOS",
                address=eosAddress.address
            )
        except CryptomarketSDKException as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()
