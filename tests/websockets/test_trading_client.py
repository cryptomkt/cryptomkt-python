import json
import time
import unittest
from typing import Optional, Union
from cryptomarket import args

from test_helpers import *

from cryptomarket.websockets import TradingClient

with open('/home/ismael/cryptomarket/keys.json') as fd:
    keys = json.load(fd)


class TestWSTradingClient(unittest.TestCase):

    def setUp(self):
        self.ws = TradingClient(
            keys['apiKey'],
            keys['apiSecret'],
            window=10_000,
            on_error=lambda err: print(err),
        )
        err = self.ws.connect(5)
        if err:
            self.fail(err)
        Veredict.reset()

    def tearDown(self):
        try:
            self.ws.close()
        except Exception as e:
            print(e)

    def test_order_flow(self):
        client_order_id = str(int(time.time()))

        def on_active_orders(err, order_list):
            if err:
                Veredict.fail(f'{err}')
                return
            if not good_report_list(order_list):
                Veredict.fail("not a good order list")
                return
            order: Report
            for order in order_list:
                if order.client_order_id == client_order_id+"new":
                    Veredict.fail('order not canceled')
                    return
            Veredict.done = True

        def on_canceled_order(err, canceled_order: Optional[Report]):
            if err:
                Veredict.fail(f'{err}')
                return
            if canceled_order is None:
                Veredict.fail(f'canceled_order is none')
                return
            if not canceled_order.report_type == 'canceled':
                Veredict.fail('order not canceled')
                return
            if not good_report(canceled_order):
                Veredict.fail('not a good report')
                return
            self.ws.get_active_spot_orders(on_active_orders)

        def on_replaced_order(err, replaced_order: Optional[Report]):
            if err:
                Veredict.fail(f'{err}')
                return
            if replaced_order is None:
                Veredict.fail(f'replaced order is none')
                return
            if not good_report(replaced_order):
                Veredict.fail("not a good report")
                return
            if not replaced_order.report_type == 'replaced':
                Veredict.fail("order not replaced")
                return
            client_order_id = replaced_order.client_order_id
            self.ws.cancel_spot_order(client_order_id, on_canceled_order)

        def on_created_order(err, created_order: Union[Report, None]):
            if err:
                Veredict.fail(f'{err}')
                return
            if created_order is None:
                Veredict.fail(f'created order is none')
                return
            if not good_report(created_order):
                Veredict.fail("not a good report")
                return
            if not created_order.status == 'new':
                Veredict.fail('not a new order')
            self.ws.replace_spot_order(
                client_order_id,
                client_order_id+"new",
                '0.01',
                '101010',
                callback=on_replaced_order,
            )

        self.ws.create_spot_order(
            client_order_id=client_order_id,
            symbol='EOSETH',
            side='sell',
            quantity='0.01',
            price='10000',
            callback=on_created_order)
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_get_trading_balances(self):
        def check_good_balances(err, balances):
            if err:
                Veredict.fail(f'{err}')
                return
            if not len(balances) > 0:
                Veredict.fail("no balances")
                return
            if not good_balances(balances):
                Veredict.fail("not good balances")
                return
            Veredict.done = True

        self.ws.get_spot_trading_balances(check_good_balances)
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_get_trading_balance_of_currency(self):
        def check_good_balance(err, balance):
            if err:
                Veredict.fail(f'{err}')
                return
            if not good_balance(balance):
                Veredict.fail("not good balance")
                return
            Veredict.done = True
        self.ws.get_spot_trading_balance_of_currency('EOS', check_good_balance)
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_get_spot_trading_commissions(self):
        def check_good_trading_commission(err, commissions):
            if err:
                Veredict.fail(f'{err}')
                return

            for commission in commissions:
                if not good_trading_commission(commission):
                    Veredict.fail('not a good commission')
                    return
            Veredict.done = True

        self.ws.get_spot_commisions(check_good_trading_commission)
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_get_spot_trading_commission_of_symbol(self):
        def check_good_trading_commission(err, commission):
            if err:
                Veredict.fail(f'{err}')
                return
            if not good_trading_commission(commission):
                Veredict.fail('not a good commission')
                return
            Veredict.done = True
        try:
            self.ws.get_spot_commision_of_symbol(
                'EOSETH', check_good_trading_commission)
        except Exception as e:
            print(e)
            self.fail(str(e))
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_create_spot_order_list(self):
        first_order_id = str(int(time.time()))
        second_order_id = first_order_id + "2"
        side = args.Side.SELL
        quantity = "0.01"
        price = "10000"
        time_in_force = args.TimeInForce.FOK

        def check_good_report(err, report):
            if err:
                Veredict.fail(f'{err}')
                return
            if not good_report(report):
                Veredict.fail('not a good report')
                return
            Veredict.done = True
        try:
            self.ws.create_spot_order_list(
                contingency_type=args.ContingencyType.ALL_OR_NONE,
                order_list_id=first_order_id,
                orders=[
                    args.OrderRequest(
                        'EOSETH',
                        side=side,
                        quantity=quantity,
                        client_order_id=first_order_id,
                        time_in_force=time_in_force,
                        price=price
                    ),
                    args.OrderRequest(
                        'EOSBTC',
                        side=side,
                        quantity=quantity,
                        client_order_id=second_order_id,
                        time_in_force=time_in_force,
                        price=price
                    ),
                ],
                callback=check_good_report)
        except Exception as e:
            print(e)
            self.fail(str(e))
        time.sleep(10)
        Veredict.wait_done()
        if Veredict.failed:
            self.fail(Veredict.message)


if __name__ == '__main__':
    unittest.main()
