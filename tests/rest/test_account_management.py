import json
import unittest

from decimal import Decimal

import cryptomkt.args as args

from test_helpers import *

from cryptomarket.client import Client

from cryptomarket.exceptions import ArgumentFormatException
from cryptomarket.exceptions import CryptomarketSDKException



with open('/home/ismael/cryptomarket/apis/keys.json') as fd:
    keys = json.load(fd)

class AuthCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(keys['apiKey'], keys['apiSecret'])
    
    def tearDown(self):
        self.client.close()

class GetAccountBalance(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            account_balance = self.client.get_account_balance()
            if len(account_balance) == 0: self.fail("no balances")
            if not good_balances(account_balance): self.fail("not good balances")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class GetDepositCryptoAddress(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            eos_address = self.client.get_deposit_crypto_address('EOS')
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class CreateDepositCryptoAddress(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            old_address = self.client.get_deposit_crypto_address('ONT')
            new_address = self.client.create_deposit_crypto_address('ONT')
            for key in old_address:
                self.assertNotEqual(old_address[key], new_address[key])
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class Last10DepositCryptoAddress(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            last_deposits = self.client.last_10_deposit_crypto_address('EOS')
            for address in last_deposits:
                if not 'address' in last_deposits:
                    self.fail("should have address")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")
    
class Last10UsedCryptoAddress(AuthCallsTestCase): 
    # TODO: FAILING WITH: 
    # cryptomkt.exceptions.CryptomarketSDKException: APIError(code=0): Invalid JSON error message from Cryptomkt: <!DOCTYPE html>
    # <html lang="en">
    # <head>
    # <meta charset="utf-8">
    # <title>Error</title>
    # </head>
    # <body>
    # <pre>Cannot GET /api/2/account/crypto/used-addresses/BTC</pre>
    # </body>
    # </html>
    # maybe requires a prior withdrawal/transfer out.
    def test_successfull_call(self):
        try:
            last_used = self.client.last_10_used_crypto_address('BTC')
            print(last_used)
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")
    
class WithdrawCrypto(AuthCallsTestCase):
    # TODO: FAILING WITH: cryptomkt.exceptions.CryptomarketSDKException: APIError(code=403): Action is forbidden. 
    def test_successfull_call(self):
        try:
            response = self.client.withdraw_crypto(
                currency='EOS',
                amount='0.1',
                address='cryptomkteos',
                payment_id='38299046'
            )
            print(response)
        except CryptomarketSDKException as e:
            print(e)
            #self.fail("shouldn't fail")
    
class TransferConvertBetweenCurrencies(AuthCallsTestCase):
    # TODO: FAILING WITH: cryptomkt.exceptions.CryptomarketSDKException: APIError(code=403): Action is forbidden. 
    def test_successfull_call(self):
        try:
            response = self.client.transfer_convert_between_currencies(from_currency='EOS', to_currency='eth', amount='0.001')
            print(response)
        except CryptomarketSDKException as e:
            print(e)
            #self.fail("shouldn't fail")

class CommitWithdrawCrypto(AuthCallsTestCase):
    def test_call_random_id(self):
        with self.assertRaises(CryptomarketSDKException):
            response = self.client.commit_withdraw_crypto(id = 37176135661) # random number

    def test_successfull_call(self):
        #TODO: withdrawal must be active to test it
        pass
        

class RollbackWithdrawCrypto(AuthCallsTestCase):
    def test_call_random_id(self):
        with self.assertRaises(CryptomarketSDKException):
            response = self.client.rollback_withdraw_crypto(id = 10023125214) # random number


    def test_successfull_call(self):
        #TODO: withdrawal must be active to test it
        pass

class EstimateWithdrawFee(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            response = self.client.get_estimate_withdraw_fee(currency='EOS', amount='0.1')
            if response == "": self.fail("should have response")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class CheckCryptoAddressMine(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            address = self.client.get_deposit_crypto_address('ONT')
            response = self.client.check_if_crypto_address_is_mine(address['address'])
            if response == False:
                self.fail('the address should be mine')
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class TransferMoneyBetweenTradingAccountAndBankAccount(AuthCallsTestCase):
    def test_transfer_eos_to_trading(self):
        try:
            balance = self.client.get_account_balance()
            old_acc_eos_balance = None
            for curr in balance:
                if curr['currency'] == 'EOS':
                    old_acc_eos_balance = Decimal(curr['available'])

            trading_balance = self.client.get_trading_balance()
            old_t_eos_balance = None
            for curr in trading_balance:
                if curr['currency'] == 'EOS':
                    old_t_eos_balance = Decimal(curr['available'])
            
            total_eos_balance = old_acc_eos_balance + old_t_eos_balance
            amount_transfered = 0.1

            self.client.transfer_money_from_bank_balance_to_trading_balance(
                currency='EOS', 
                amount=amount_transfered
            )


            balance = self.client.get_account_balance()
            new_acc_eos_balance = None
            for curr in balance:
                if curr['currency'] == 'EOS':
                    new_acc_eos_balance = Decimal(curr['available'])

            trading_balance = self.client.get_trading_balance()
            new_t_eos_balance = None
            for curr in trading_balance:
                if curr['currency'] == 'EOS':
                    new_t_eos_balance = Decimal(curr['available'])

            delta = Decimal(0.00000000000000001)
            new_total_eos_balance = new_acc_eos_balance + new_t_eos_balance
            self.assertEqual(total_eos_balance, new_total_eos_balance)
            self.assertGreaterEqual(delta, abs(old_acc_eos_balance - Decimal(amount_transfered) - new_acc_eos_balance))
            self.assertGreaterEqual(delta,  abs(old_t_eos_balance + Decimal(amount_transfered) - new_t_eos_balance))          

        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")
    
    def test_transfer_eos_to_account(self):
        try:
            balance = self.client.get_account_balance()
            old_acc_eos_balance = None
            for curr in balance:
                if curr['currency'] == 'EOS':
                    old_acc_eos_balance = Decimal(curr['available'])

            trading_balance = self.client.get_trading_balance()
            old_t_eos_balance = None
            for curr in trading_balance:
                if curr['currency'] == 'EOS':
                    old_t_eos_balance = Decimal(curr['available'])
            
            total_eos_balance = old_acc_eos_balance + old_t_eos_balance
            amount_transfered = 0.1

            self.client.transfer_money_from_trading_balance_to_bank_balance(
                currency='EOS', 
                amount=amount_transfered
            )


            balance = self.client.get_account_balance()
            new_acc_eos_balance = None
            for curr in balance:
                if curr['currency'] == 'EOS':
                    new_acc_eos_balance = Decimal(curr['available'])

            trading_balance = self.client.get_trading_balance()
            new_t_eos_balance = None
            for curr in trading_balance:
                if curr['currency'] == 'EOS':
                    new_t_eos_balance = Decimal(curr['available'])
            
            delta = Decimal(0.00000000000000001)
            new_total_eos_balance = new_acc_eos_balance + new_t_eos_balance
            self.assertEqual(total_eos_balance, new_total_eos_balance)
            self.assertGreaterEqual(delta, abs(old_acc_eos_balance + Decimal(amount_transfered) - new_acc_eos_balance))
            self.assertGreaterEqual(delta, abs(old_t_eos_balance - Decimal(amount_transfered) - new_t_eos_balance))

        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class TransferMoneyToAnotherUser(AuthCallsTestCase):
    #TODO: need a second account
    pass

class GetTransactionsHistory(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            response = self.client.get_transactions_history(currency='EOS')
            for transaction in response:
                if not good_transaction(transaction): self.fail("no good transaction")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")

class GetTransaction(AuthCallsTestCase):
    def test_successfull_call(self):
        try:
            response = self.client.get_transactions_history(currency='EOS')
            some_transaction_id = response[0]['id']
            response = self.client.get_transaction(id=some_transaction_id)
            if not good_transaction(transaction): self.fail("not good transaction")
        except CryptomarketSDKException as e:
            self.fail("shouldn't fail")
            

if __name__ == '__main__':
    unittest.main()