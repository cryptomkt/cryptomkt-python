import json
import unittest
from datetime import datetime

from test_helpers import *

import cryptomarket.args as args
from cryptomarket.client import Client
from cryptomarket.exceptions import CryptomarketSDKException


def pprint(a_json_obj):
    print('')
    v_s = json.dumps(a_json_obj, indent=4)
    print(v_s)
    print('')


class Key_printer:
    def __init__(self):
        self.keys = []

    def add_keys(self, a_dict):
        for key in a_dict:
            self.keys.append(key)

    def print_keys(self):
        print('')
        print('')
        for key in self.keys:
            print(key)
        print('')


class PublicCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client('', '')

    def tearDown(self):
        self.client.close()


class GetCurrencies(PublicCallsTestCase):
    def test_get_all_currencies(self):
        try:
            currencies = self.client.get_currencies()
            if len(currencies) == 0:
                self.fail("no currencies")
            for currency_ID in currencies:
                if not good_currency(currencies[currency_ID]):
                    self.fail("not a good currency")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

    def test_get_many_currencies(self):
        try:
            currencies = self.client.get_currencies(['ETH', 'BTC'])
            if len(currencies) != 2:
                self.fail("not right number of currencies")
            for currencyID in currencies:
                if not good_currency(currencies[currencyID]):
                    self.fail("not a good currency")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

    def test_get_one_currency(self):
        try:
            currencies = self.client.get_currencies(['USDT'])
            if len(currencies) != 1:
                self.fail("not right number of currencies")
            for currencyID in currencies:
                if not good_currency(currencies[currencyID]):
                    self.fail("not a good currency")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")


class GetCurrency(PublicCallsTestCase):
    def test_get_currency(self):
        try:
            currency = self.client.get_currency('USDT')
            if not good_currency(currency):
                self.fail("not a good currency")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")


class GetSymbols(PublicCallsTestCase):
    def test_get_all_symbols(self):
        symbols = self.client.get_symbols()
        if len(symbols) == 0:
            self.fail("no symbols")
        for symbolID in symbols:
            if not good_symbol(symbols[symbolID]):
                self.fail(f"not a good symbol: {symbols[symbolID]}")

    def test_get_many_symbols(self):
        symbols = self.client.get_symbols(['COMPUSDT', 'EURSDAI'])
        if len(symbols) != 2:
            self.fail("not right number of symbols")
        for symbolID in symbols:
            if not good_symbol(symbols[symbolID]):
                self.fail("not a good symbol")

    def test_get_one_symbol(self):
        symbols = self.client.get_symbols(['ETHBTC'])
        if len(symbols) != 1:
            self.fail("not right number of symbols")
        for symbolID in symbols:
            if not good_symbol(symbols[symbolID]):
                self.fail("not a good symbol")


class GetSymbol(PublicCallsTestCase):
    def test_get_symbol(self):
        symbol = self.client.get_symbol('ETHBTC')
        if not good_symbol(symbol):
            self.fail("not a good symbol")


class GetTickers(PublicCallsTestCase):
    def test_get_all_tickers(self):
        tickers = self.client.get_tickers()
        if len(tickers) == 0:
            self.fail("no tickers")
        for tickerID in tickers:
            if not good_ticker(tickers[tickerID]):
                self.fail("not a good ticker")

    def test_get_many_ticker(self):
        tickers = self.client.get_tickers(['ETHBTC', 'ETHUSDT'])
        if len(tickers) != 2:
            self.fail("not right number of tickers")
        for tickerID in tickers:
            if not good_ticker(tickers[tickerID]):
                self.fail("not a good ticker")

    def test_get_one_ticker(self):
        tickers = self.client.get_tickers(['ETHBTC'])
        if len(tickers) != 1:
            self.fail("not right number of tickers")
        for tickerID in tickers:
            if not good_ticker(tickers[tickerID]):
                self.fail("not a good ticker")


class GetTicker(PublicCallsTestCase):
    def test_get_ticker(self):
        ticker = self.client.get_ticker('ETHBTC')
        if not good_ticker(ticker):
            self.fail("not a good ticker")


class GetPrices(PublicCallsTestCase):
    def test_get_prices(self):
        prices = self.client.get_prices("ETH", "BTC")
        if len(prices) != 1:
            self.fail("not right number of prices")
        for priceID in prices:
            if not good_price(prices[priceID]):
                self.fail("not a good price")

    def test_get_all_prices(self):
        prices = self.client.get_prices("ETH")
        if len(prices) < 1:
            self.fail("not right number of prices")
        for priceID in prices:
            if not good_price(prices[priceID]):
                self.fail("not a good price")


class GetPricesHistory(PublicCallsTestCase):
    def test_get_price_history(self):
        history = self.client.get_prices_history("ETH")
        for currency in history:
            if not good_price_history(history[currency]):
                self.fail("not a good price history")

    def test_get_some_price_history(self):
        history = self.client.get_prices_history(
            "ETH", "BTC", period=args.Period._15_MINS, sort=args.Sort.ASCENDING)
        if len(history) != 1:
            self.fail("not rith number of prices")
        for currency in history:
            if not good_price_history(history[currency]):
                self.fail("not a good price history")


class GetTickerPrices(PublicCallsTestCase):
    def test_get_ticker_prices(self):
        prices = self.client.get_ticker_last_prices()
        if len(prices) < 2:
            self.fail("too low number of prices")
        for priceID in prices:
            if not good_ticker_price(prices[priceID]):
                self.fail("not a good price")

    def test_get_some_ticker_prices(self):
        prices = self.client.get_ticker_last_prices(["EOSETH", "XLMETH"])
        if len(prices) != 2:
            self.fail("too low number of prices")
        for priceID in prices:
            if not good_ticker_price(prices[priceID]):
                self.fail("not a good price")


class GetTickerPricesOfSymbol(PublicCallsTestCase):
    def test_get_ticker_price(self):
        price = self.client.get_ticker_last_price_of_symbol("EOSETH")
        if not good_ticker_price(price):
            self.fail("not a good price")


class GetTrades(PublicCallsTestCase):
    def test_get_trades_of_all_symbols(self):
        trades = self.client.get_trades()
        for key in trades:
            if not good_list(good_public_trade, trades[key]):
                self.fail("not a good trade")

    def test_get_trades_of_many_symbols(self):
        trades = self.client.get_trades(['ETHBTC', 'ETHUSDT'], limit=2)
        self.assertEqual(
            len(trades), 2, 'should have trades from only two symbols')
        for key in trades:
            if not good_list(good_public_trade, trades[key]):
                self.fail("not a good trade")

    def test_get_trades_of_one_symbol(self):
        trades = self.client.get_trades(['ETHBTC'])
        self.assertEqual(
            len(trades), 1, 'should have trades from only one symbol')
        for key in trades:
            if not good_list(good_public_trade, trades[key]):
                self.fail("not a good trade")

    def test_asc_sorted(self):
        trades = self.client.get_trades(sort=args.Sort.ASCENDING)

    def test_limit_10(self):
        trades = self.client.get_trades(['ETHBTC'], limit=10)
        self.assertEqual(len(trades['ETHBTC']), 10, 'should have 10 trades')

    def test_since_wrong_format_raise_exception(self):
        with self.assertRaises(CryptomarketSDKException):
            trades = self.client.get_trades(since='yesterday')

    def test_since_iso_format(self):
        iso_datetime = datetime(
            year=2020,
            month=9,
            day=19).isoformat()
        trades = self.client.get_trades(since=iso_datetime)

    def test_since_id(self):
        trades = self.client.get_trades(since=1005147907)


class GetOrderBooks(PublicCallsTestCase):
    def test_get_all_symbols(self):
        orderbooks = self.client.get_order_books()
        for key in orderbooks:
            orderbook_of_symbol = orderbooks[key]
            if not good_orderbook(orderbook_of_symbol):
                self.fail("not a good orderbook")

    def test_get_many_symbols(self):
        orderbooks = self.client.get_order_books(
            symbols=['ETHBTC', 'ETHUSDT'])
        self.assertEqual(len(orderbooks), 2, "should have two orderbooks")
        for key in orderbooks:
            orderbook_of_symbol = orderbooks[key]
            if not good_orderbook(orderbook_of_symbol):
                self.fail("not a good orderbook")

    def test_one_symbol(self):
        orderbooks = self.client.get_order_books(symbols=['ETHBTC'])
        self.assertEqual(len(orderbooks), 1, "should have one orderbook")
        for key in orderbooks:
            orderbook_of_symbol = orderbooks[key]
            if not good_orderbook(orderbook_of_symbol):
                self.fail("not a good orderbook")


class GetOrderBookOfSymbol(PublicCallsTestCase):
    def test_get_orderbook(self):
        orderbook = self.client.get_order_book_of_symbol(symbol='ETHBTC')
        if not good_orderbook(orderbook):
            self.fail("not a good orderbook")


class GetOrderBookVolumeOfSymbol(PublicCallsTestCase):
    def test_get_orderbook(self):
        orderbook = self.client.get_order_book_volume_of_symbol(
            symbol='ETHBTC',
            volume='100'
        )
        if not good_orderbook(orderbook):
            self.fail("not a good orderbook")


class GetCandles(PublicCallsTestCase):
    def test_get_all_symbols(self):
        candles = self.client.get_candles()
        for key in candles:
            if not good_list(good_candle, candles[key]):
                self.fail("not good candles")

    def test_get_many_symbols(self):
        candles = self.client.get_candles(
            symbols=['ETHBTC', 'ETHUSDT'], limit=2)
        self.assertEqual(len(candles), 2, "should have two candles")

    def test_one_symbol(self):
        candles = self.client.get_candles(symbols=['ETHBTC'])
        self.assertEqual(len(candles), 1, "should have one candles")


class GetConvertedCandles(PublicCallsTestCase):
    def test_get_all_symbols(self):
        target_currency = "BTC"
        converted_candles = self.client.get_converted_candles(target_currency)
        self.assertEqual(converted_candles.target_currency, target_currency)
        for key in converted_candles.data:
            if not good_list(good_candle, converted_candles.data[key]):
                self.fail("not good candles")

    def test_get_many_symbols(self):
        target_currency = "BTC"
        converted_candles = self.client.get_converted_candles(
            target_currency, ["EOSETH", "ETHBTC", "CROBTC"])
        self.assertEqual(converted_candles.target_currency, target_currency)
        for key in converted_candles.data:
            if not good_list(good_candle, converted_candles.data[key]):
                self.fail("not good candles")
        self.assertEqual(len(converted_candles.data),
                         3, "should have two candles")

    def test_one_symbol(self):
        target_currency = "BTC"
        converted_candles = self.client.get_converted_candles(
            target_currency, ["CROBTC"])
        self.assertEqual(converted_candles.target_currency, target_currency)
        for key in converted_candles.data:
            if not good_list(good_candle, converted_candles.data[key]):
                self.fail("not good candles")
        self.assertEqual(len(converted_candles.data),
                         1, "should have two candles")


class GetConvertedCandlesOfSymbol(PublicCallsTestCase):
    def test_get_all_symbols(self):
        target_currency = "BTC"
        converted_candles = self.client.get_converted_candles_of_symbol(
            target_currency, symbol="CROETH")
        self.assertEqual(converted_candles.target_currency, target_currency)
        if not good_list(good_candle, converted_candles.data):
            self.fail("not good candles")


if __name__ == '__main__':
    unittest.main()
