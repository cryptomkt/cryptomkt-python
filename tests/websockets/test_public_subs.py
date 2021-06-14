import json
import time
import unittest
import datetime

import cryptomarket.args as args

from test_helpers import *

from cryptomarket.websockets import PublicClient

second = 1
minute = 60

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

class TestWSClientPublicSubs(unittest.TestCase):

    def setUp(self):
        self.ws = PublicClient(on_error=lambda err: print(err))
        self.ws.connect()
    
    def tearDown(self):
        self.ws.close()
        time.sleep(5 * second)
    
    def test_subscribe_to_tickers(self):
        def fail_on_err(err, success):
            if err is not None:
                self.fail("error in the request")
            
        symbol = 'EOSETH'
        checker = TimeFLow()
        def check_timestamps(feed):
            if not good_ticker(feed): 
                self.fail("not good ticker")
            if not checker.check_next_time(feed['timestamp']):
                self.fail("wrong ticker order")
                
        self.ws.subscribe_to_ticker(symbol, check_timestamps, fail_on_err)
        time.sleep(2 * minute)
        self.ws.unsubscribe_to_ticker(symbol, fail_on_err)
        time.sleep(5 * second)

    def test_subscribe_to_orderbook(self):
        def fail_on_err(err, success):
            if err is not None:
                self.fail("error in the request")
        checker = SequenceFlow()
        def check_valid_book(book):
            if not good_orderbook(book): self.fail("not a good orderbook")
            checker.check_next_sequence(book['timestamp'])
            for side in ['ask', 'bid']:
                for level in book[side]:
                    if level['size'] == '0.00': 
                        self.fail("size of 0")
            
        self.ws.subscribe_to_order_book('ETHBTC', check_valid_book, fail_on_err)
        time.sleep(3 * minute)
        self.ws.unsubscribe_to_order_book('ETHBTC', fail_on_err)
        time.sleep(5 * second)

    def test_subscribe_to_trades(self):
        def fail_on_err(err, success):
            if err is not None:
                self.fail("error in the request")
        
        def check_good_p_trades(trades):
            for trade in trades:
                if not good_public_trade(trade):
                    self.fail("not good public trade")
            
        self.ws.subscribe_to_trades('ETHBTC', check_good_p_trades, result_callback=fail_on_err)
        time.sleep(2 * minute)
        self.ws.unsubscribe_to_trades('ETHBTC', fail_on_err)
        time.sleep(5 * second)

    def test_subscribe_to_candles(self):
        def fail_on_err(err, success):
            if err is not None:
                self.fail("error in the request")
        
        def check_good_p_trades(candles):
            if not good_candle_list(candles):
                self.fail("not good candles")

        self.ws.subscribe_to_candles('EOSETH', args.PERIOD._1_MINS, check_good_p_trades, result_callback=fail_on_err)
        time.sleep(2 * minute)
        self.ws.unsubscribe_to_candles('EOSETH', args.PERIOD._1_MINS, fail_on_err)
        time.sleep(5 * second)
    
    def test_subscribe_twice_to_candles(self):
        result_callback = lambda err, result: self.assertTrue(result) if err is not None else self.fail()
        self.ws.subscribe_to_candles('EOSETH', args.PERIOD._1_MINS, lambda feed: print(feed), 1, result_callback)
        time.sleep(5 * second)
        self.ws.subscribe_to_candles('EOSETH', args.PERIOD._1_MINS, lambda feed: print(feed), 1, result_callback)
        time.sleep(5 * second)
        self.ws.unsubscribe_to_candles('EOSETH', args.PERIOD._1_MINS, result_callback)
        time.sleep(5 * second)
        self.ws.unsubscribe_to_candles('EOSETH', args.PERIOD._1_MINS, result_callback)
        time.sleep(5 * second)
        

if __name__ == '__main__':
    unittest.main()