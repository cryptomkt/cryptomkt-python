import json
import time
import unittest
from typing import Optional

from test_helpers import *

from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.websockets import TradingClient

minute = 60
second = 1

with open('/home/ismael/cryptomarket/keys.json') as fd:
    keys = json.load(fd)


def failOnError(caller: str):
    def f(err: Optional[CryptomarketAPIException], result):
        if err:
            Veredict.fail(caller + ": " + err.message)
    return f


class TestWSClientTradingSubs(unittest.TestCase):

    def setUp(self):
        self.ws = TradingClient(
            keys['apiKey'], keys['apiSecret'], on_error=lambda err: print(err) if err else None)
        err = self.ws.connect(3)
        if err:
            print("connection failed")
            print(err)
            self.fail()
        Veredict.reset()

    def tearDown(self):
        self.ws.close()

    def test_subscribe_to_reports(self):
        def callback(feed, feed_type):
            for report in feed:
                if not good_report(report):
                    Veredict.fail('not a good report')
                    return
        self.ws.subscribe_to_reports(
            callback, failOnError('subscribe to reports'))
        time.sleep(5 * second)
        client_order_id = str(int(time.time()*1000))
        self.ws.create_spot_order(
            'EOSETH',
            'sell',
            '0.1',
            client_order_id=client_order_id,
            price='10000',
            callback=failOnError('create spot order')
        )
        time.sleep(5 * second)
        self.ws.cancel_spot_order(
            client_order_id,
            callback=failOnError('cancel spot order')
        )
        time.sleep(5 * second)
        self.ws.unsubscribe_to_reports(failOnError('unsubscribe to reports'))
        time.sleep(5 * second)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_spot_balance(self):
        def callback(feed: List[Balance]):
            if not good_balances(feed):
                Veredict.fail('not a good balance')
                return
        self.ws.subscribe_to_spot_balance(
            mode='batches',
            callback=callback,
            result_callback=failOnError('subscribe to spot balance')
        )
        time.sleep(5 * second)
        client_order_id = str(int(time.time()*1000))
        self.ws.create_spot_order(
            'EOSETH',
            'sell',
            '0.1',
            client_order_id=client_order_id,
            price='10000',
            callback=failOnError('create spot order')
        )
        time.sleep(5 * second)
        self.ws.cancel_spot_order(
            client_order_id,
            callback=failOnError('cancel spot order')
        )
        time.sleep(5 * second)
        self.ws.unsubscribe_to_spot_balance(
            callback=failOnError('unsubscribe to spot balance')
        )
        time.sleep(5 * second)
        if Veredict.failed:
            self.fail(Veredict.message)


if __name__ == '__main__':
    unittest.main()
