import json
import time
import unittest
from cryptomarket.dataclasses.order import OrderStatus

from test_helpers import *

import cryptomarket.args as args
from cryptomarket.client import Client
from cryptomarket.exceptions import CryptomarketSDKException

with open('/home/ismael/cryptomarket/keys.json') as fd:
    keys = json.load(fd)


class AuthCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(keys['apiKey'], keys['apiSecret'])

    def tearDown(self):
        self.client.close()


class GetTradingBalance(AuthCallsTestCase):
    def test_successfull_call(self):
        trading_balances = self.client.get_spot_trading_balances()
        print("**balances**")
        print(trading_balances)
        if len(trading_balances) == 0:
            self.fail("no balances")
        if not good_list(good_balance, trading_balances):
            self.fail("not good balance")


class GetTradingBalanceOfCurrency(AuthCallsTestCase):
    def test_successfull_call(self):
        trading_balances = self.client.get_spot_trading_balance_of_currency(
            "CRO")
        if not good_balance(trading_balances):
            self.fail("not good balance")


class CreateOrder(AuthCallsTestCase):
    # default on optional arguments, ('price' required on 'limit' orders, the default type)
    def test_create_order_default_arguments(self):
        new_order = self.client.create_spot_order(
            symbol='EOSETH',
            side='sell',
            quantity='0.01',
            price="1000",
        )
        if not good_order(new_order):
            self.fail("not good order")

    def test_exception_for_selling_nothing(self):
        with self.assertRaises(CryptomarketSDKException):
            new_order = self.client.create_spot_order(
                symbol='EOSETH',
                side='sell',
                type='limit',
                quantity='0',
                price="1000",
            )


class GetActiveOrders(AuthCallsTestCase):
    def test_successfull_call(self):
        active_orders = self.client.get_all_active_spot_orders()
        if not good_list(good_order, active_orders):
            self.fail("not good orders")

    def test_filter_by_symbol(self):
        active_orders = self.client.get_all_active_spot_orders(
            symbol='EOSETH')
        if not good_list(good_order, active_orders):
            self.fail("not good order")


class OrderFlow(AuthCallsTestCase):
    def test_wrong_id_call(self):
        with self.assertRaises(CryptomarketSDKException):
            self.client.get_active_spot_order(
                client_order_id='123')

    def test_successfull_call(self):  # create order should work properly
        # create
        client_order_id = str(int(time.time()))
        order = self.client.create_spot_order(
            symbol='EOSETH',
            side=args.Side.SELL,
            quantity='0.01',
            client_order_id=client_order_id,
            price='1000')
        print(order)
        if not good_order(order):
            self.fail("not good order")
        # get
        order = self.client.get_active_spot_order(client_order_id)
        if not good_order(order):
            self.fail("not good order")

        # replace
        new_client_order_id = str(int(time.time()))+"1"
        self.client.replace_spot_order(
            client_order_id=order.client_order_id,
            new_client_order_id=new_client_order_id,
            quantity="0.02",
            price='100'
        )
        if not good_order(order):
            self.fail("not good order")

        # cancel
        order = self.client.cancel_spot_order(new_client_order_id)
        if not good_order(order):
            self.fail("not good order")


class CancellAllActiveOrders(AuthCallsTestCase):
    def test_successfull_call(self):
        for i in range(3):
            self.client.create_spot_order(
                symbol='EOSETH',
                side=args.Side.SELL,
                quantity='0.01',
                type=args.OrderType.LIMIT,
                price='1000'
            )

        orders = self.client.get_all_active_spot_orders(symbol='EOSETH')
        self.assertTrue(len(orders) >= 3, 'should have at least 3 orders')

        self.client.cancel_all_orders(symbol='EOSETH')

        orders_after_cancel = self.client.get_all_active_spot_orders(
            symbol='EOSETH')
        self.assertTrue(len(orders_after_cancel) == 0, "shouldn't have orders")


class CancelOrderByClientId(AuthCallsTestCase):
    def test_successfull_call(self):
        order = self.client.create_spot_order(
            symbol='EOSETH',
            side=args.Side.SELL,
            quantity='0.01',
            type=args.OrderType.LIMIT,
            price='1000'
        )
        client_order_id = order.client_order_id
        response = self.client.cancel_spot_order(client_order_id)
        if not good_order(response):
            self.fail("Not good order")

        with self.assertRaises(CryptomarketSDKException):
            order = self.client.get_active_spot_order(client_order_id)



class CancelOrderByClientId(AuthCallsTestCase):
    def test_successfull_call(self):
        order = self.client.create_spot_order(
            symbol='ADAUSDT',
            side=args.Side.BUY,
            quantity='5',
            type=args.OrderType.LIMIT,
            price='0.1'
        )
        assert(order.status == OrderStatus.NEW)
        time.sleep(5)
        canceled_order = self.client.cancel_spot_order(order.client_order_id)
        assert(canceled_order.status == OrderStatus.CANCELED)



class GetAllTradingCommissions(AuthCallsTestCase):
    def test_successfull_call(self):
        result = self.client.get_all_trading_commissions()
        if not good_list(good_trading_commission, result):
            self.fail("not valid trading commision")


class GetTradingCommission(AuthCallsTestCase):
    def test_successfull_call(self):
        commission = self.client.get_trading_commission('EOSETH')
        if not good_trading_commission(commission):
            self.fail("not valid trading commision")


class CancelingOrders(AuthCallsTestCase):
    def test_cancel_all_with_arguments(self):
        self.client.cancel_all_orders()
        self.client.create_spot_order(
            symbol='EOSETH',
            side='sell',
            quantity='0.01',
            price='1001',
        )
        self.client.create_spot_order(
            symbol='EOSBTC',
            side='sell',
            quantity='0.01',
            price='1001',
        )
        response = self.client.cancel_all_orders('EOSETH')
        if len(response) == 2:
            self.fail("should only cancel one order")
        self.client.cancel_all_orders()


class OrderList(AuthCallsTestCase):
    def test_create_order_list(self):
        orders = self.client.create_spot_order_list(
            args.ContingencyType.ALL_OR_NONE,
            [args.OrderRequest(
                symbol="EOSETH",
                side=args.Side.SELL,
                type=args.OrderType.LIMIT,
                time_in_force=args.TimeInForce.FOK,
                quantity="0.1",
                price="10000"),
             args.OrderRequest(
                symbol="EOSUSDT",
                side=args.Side.SELL,
                type=args.OrderType.LIMIT,
                time_in_force=args.TimeInForce.FOK,
                quantity="0.1",
                price="10000")])
        print(orders)
        if not good_list(good_order, orders):
            self.fail("not valid orders: " + orders)
        self.client.cancel_all_orders()


if __name__ == '__main__':
    unittest.main()
