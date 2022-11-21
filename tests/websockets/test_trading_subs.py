import json
import time
import unittest

from cryptomarket.websockets import TradingClient

from test_helpers import *

minute = 60
second = 1

with open('/home/ismael/cryptomarket/keys-v3.json') as fd:
    keys = json.load(fd)


class TestWSClientTradingSubs(unittest.TestCase):

    def setUp(self):
        self.ws = TradingClient(
            keys['apiKey'], keys['apiSecret'], on_error=lambda err: print(err))
        self.ws.connect()
        Veredict.reset()

    def tearDown(self):
        self.ws.close()

    def test_subscribe_to_reports(self):
        def callback(feed, feed_type):
            for report in feed:
                if not good_report(report):
                    Veredict.fail('not a good report')
                    return
        self.ws.subscribe_to_reports(callback)
        time.sleep(5 * second)
        client_order_id = str(int(time.time()*1000))
        self.ws.create_spot_order(
            'EOSETH',
            'sell',
            '0.1',
            client_order_id=client_order_id,
            price='10000',
            callback=lambda err, result: print(err)
        )
        time.sleep(5 * second)
        self.ws.cancel_spot_order(
            client_order_id,
            callback=lambda err, result: print(err)
        )
        time.sleep(5 * second)
        self.ws.unsubscribe_to_reports()
        if Veredict.failed:
            self.fail(Veredict.message)


if __name__ == '__main__':
    unittest.main()
