import time
import unittest

import cryptomarket.args as args
from cryptomarket.websockets import MarketDataClient

from test_helpers import *

SECOND = 1
MINUTE = 60


def result_callback(err, symbol_list):
    if err:
        Veredict.fail(f'error:{err}')


class TestWSClientPublicSubs(unittest.TestCase):

    def setUp(self):
        self.ws = MarketDataClient(on_error=lambda err: print(err))
        self.ws.connect()
        Veredict.reset()

    def tearDown(self):
        self.ws.close()
        time.sleep(5 * SECOND)

    def test_subscribe_to_trades(self):
        def callback(trades_by_symbol: Dict[str, List[WSTrade]], notification_type):
            for symbol in trades_by_symbol:
                trade_list = trades_by_symbol[symbol]
                if not good_list(good_wstrade, trade_list):
                    Veredict.fail("not a good trade list")
        self.ws.subscribe_to_trades(
            callback=callback,
            symbols=['ETHBTC'],
            limit=5,
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_candles(self):
        def callback(candles_of_symbol: Dict[str, List[WSCandle]], notification_type: str):
            for symbol in candles_of_symbol:
                candles = candles_of_symbol[symbol]
                if not good_candle_list(candles):
                    Veredict.fail("not a good candle list")
        self.ws.subscribe_to_candles(
            callback=callback,
            symbols=['ETHBTC'],
            period=args.PERIOD._1_MINS,
            limit=19,
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_mini_ticker(self):
        def callback(minitickers_of_symbol: Dict[str, WSMiniTicker]):
            for symbol in minitickers_of_symbol:
                mini_ticker = minitickers_of_symbol[symbol]
                if not good_mini_ticker(mini_ticker):
                    Veredict.fail("not a good mini ticker")
        self.ws.subscribe_to_mini_ticker(
            callback=callback,
            symbols=['ETHBTC'],
            speed=args.TICKER_SPEED._3_SECONDS,
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_mini_ticker_batch(self):
        def callback(minitikers_of_symbol: Dict[str, WSMiniTicker]):
            for symbol in minitikers_of_symbol:
                ticker = minitikers_of_symbol[symbol]
                if not good_mini_ticker(ticker):
                    Veredict.fail("not a good mini ticker")
        self.ws.subscribe_to_mini_ticker_in_batch(
            callback=callback,
            symbols=['ETHBTC'],
            speed=args.TICKER_SPEED._3_SECONDS,
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_ticker(self):
        def callback(tikers_of_symbol: Dict[str, WSTicker]):
            for symbol in tikers_of_symbol:
                ticker = tikers_of_symbol[symbol]
                if not good_wsticker(ticker):
                    Veredict.fail("not a good mini ticker")
        self.ws.subscribe_to_ticker(
            callback=callback,
            speed=args.TICKER_SPEED._3_SECONDS,
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_ticker_batch(self):
        def callback(tikers_of_symbol: Dict[str, WSTicker]):
            for symbol in tikers_of_symbol:
                ticker = tikers_of_symbol[symbol]
                if not good_wsticker(ticker):
                    Veredict.fail("not a good mini ticker")
        self.ws.subscribe_to_ticker_in_batch(
            callback=callback,
            speed=args.TICKER_SPEED._3_SECONDS,
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_full_order_book(self):
        def callback(orderbooks_of_symbol: Dict[str, WSOrderBook], notification_type: str):
            for symbol in orderbooks_of_symbol:
                order_book = orderbooks_of_symbol[symbol]
                if not good_wsorder_book(order_book):
                    Veredict.fail("not a good mini ticker")
        self.ws.subscribe_to_full_order_book(
            callback=callback,
            symbols=['EOSETH'],
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_partial_order_book(self):
        def callback(orderbooks_of_symbol: Dict[str, WSOrderBook]):
            for symbol in orderbooks_of_symbol:
                order_book = orderbooks_of_symbol[symbol]
                if not good_wsorder_book(order_book):
                    Veredict.fail("not a good mini ticker")
        self.ws.subscribe_to_partial_order_book(
            callback=callback,
            depth=args.DEPTH._5,
            speed=args.ORDERBOOK_SPEED._100_MILISECONDS,
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)

    def test_subscribe_to_top_of_order_book(self):
        def callback(top_of_orderbooks_of_symbol: Dict[str, WSOrderBookTop]):
            for symbol in top_of_orderbooks_of_symbol:
                top_of_order_book = top_of_orderbooks_of_symbol[symbol]
                if not good_orderbook_top(top_of_order_book):
                    Veredict.fail("not a good mini ticker")
        self.ws.subscribe_to_top_of_book(
            callback=callback,
            speed=args.ORDERBOOK_SPEED._100_MILISECONDS,
            result_callback=result_callback
        )
        time.sleep(20*SECOND)
        if Veredict.failed:
            self.fail(Veredict.message)


if __name__ == '__main__':
    unittest.main()
