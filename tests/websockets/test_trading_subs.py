import json
import time
import unittest
import datetime

import cryptomarket.args as args

from test_helpers import *

from cryptomarket.websockets import TradingClient

minute = 60
second = 1

with open('/home/ismael/cryptomarket/apis/keys.json') as fd:
    keys = json.load(fd)

class SequenceFlow:
    def __init__(self):
        self.last_sequence = None

    def check_next_sequence(self, sequence):
        good_flow = True
        if self.last_sequence is not None and sequence - self.last_sequence != 1:
            print('failing time: ', time.time())
            print(f'last: {self.last_sequence}\tactual: {sequence}')
            good_flow = False
        self.last_sequence = sequence
        return good_flow

class TimeFLow:
    def __init__(self):
        self.old_time = None
    
    def check_next_time(self, next_time):
        good_flow = True
        if self.old_time is not None and self.old_time > next_time:
            self.old_time = next_time
            good_flow = False
        self.old_time = next_time
        return good_flow

class TestWSClientTradingSubs(unittest.TestCase):

    def setUp(self):
        self.ws = TradingClient(keys['apiKey'], keys['apiSecret'], on_error=lambda err: print(err))
        self.ws.connect()
    
    def tearDown(self):
        self.ws.close()
    
    def test_subscribe_to_reports(self):
        def print_feed(feed):
            print(feed)
        self.ws.subscribe_to_reports(print_feed)
        time.sleep(5 * second)
        client_order_id = str(time.time())
        self.ws.create_order(
            client_order_id,
            'EOSETH',
            'sell',
            '0.1',
            price='10000')
        time.sleep(5 * second)
        self.ws.cancel_order(client_order_id)
        time.sleep(5 * second)


if __name__ == '__main__':
    unittest.main()