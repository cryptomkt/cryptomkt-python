import unittest

from datetime import datetime

import cryptomarket.args as args

from test_helpers import *

from cryptomarket.client import Client

from cryptomarket.exceptions import ArgumentFormatException
from cryptomarket.exceptions import CryptomarketSDKException


class PublicCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client('', '')
    
    def tearDown(self):
        self.client.close()

class GetSymbols(PublicCallsTestCase):
    def test_get_all_symbols(self):
        try:
            symbols = self.client.get_symbols()
            if len(symbols) == 0: self.fail("no symbols")
            for symbol in symbols:
                if not good_symbol(symbol):
                    self.fail("not a good symbol")
        except Exception as e:
            self.fail("shouldn't raise error "+ e)
    
    def test_get_many_symbols(self):
        try:
            symbols = self.client.get_symbols(['ETHBTC', 'ETHEUR'])
            if len(symbols) != 2: self.fail("not right number of symbols")
            for symbol in symbols:
                if not good_symbol(symbol):
                    self.fail("not a good symbol")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
    
    def test_get_one_symbol(self):
        try:
            symbols = self.client.get_symbols(['ETHBTC'])
            if len(symbols) != 1: self.fail("not right number of symbols")
            for symbol in symbols:
                if not good_symbol(symbol):
                    self.fail("not a good symbol")

        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

class GetSymbol(PublicCallsTestCase):
    def test_get_symbol(self):
        try:
            symbol = self.client.get_symbol('ETHBTC')
            if not good_symbol(symbol):
                self.fail("not a good symbol")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

class GetCurrencies(PublicCallsTestCase):
    def test_get_all_currencies(self):
        try:
            currencies = self.client.get_currencies()
            if len(currencies) == 0: self.fail("no currencies")
            for currency in currencies:
                if not good_currency(currency):
                    print(currency.keys())
                    self.fail("not a good currency")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
    
    def test_get_many_currencies(self):
        try:
            currencies = self.client.get_currencies(['ETH', 'BTC'])
            if len(currencies) != 2: self.fail("not right number of currencies")
            for currency in currencies:
                if not good_currency(currency):
                    self.fail("not a good currency")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
    
    def test_get_one_currency(self):
        try:
            currencies = self.client.get_currencies(['USD'])
            if len(currencies) != 1: self.fail("not right number of currencies")
            for currency in currencies:
                if not good_currency(currency):
                    self.fail("not a good currency")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

class GetCurrency(PublicCallsTestCase):
    def test_get_currency(self):
        try:
            currency = self.client.get_currency('USD')
            if not good_currency(currency):
                self.fail("not a good currency")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

class GetTickers(PublicCallsTestCase):
    def test_get_all_tickers(self):
        try:
            tickers = self.client.get_tickers()
            if len(tickers) == 0: self.fail("no tickers")
            for ticker in tickers:
                if not good_ticker(ticker):
                    self.fail("not a good ticker")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
    
    def test_get_many_ticker(self):
        try: 
            tickers = self.client.get_tickers(['ETHBTC', 'ETHUSD'])
            if len(tickers) != 2: self.fail("not right number of tickers")
            for ticker in tickers:
                if not good_ticker(ticker):
                    self.fail("not a good ticker")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

    def test_get_one_ticker(self):
        try: 
            tickers = self.client.get_tickers(['ETHBTC'])
            if len(tickers) != 1: self.fail("not right number of tickers")
            for ticker in tickers:
                if not good_ticker(ticker):
                    self.fail("not a good ticker")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

class GetTicker(PublicCallsTestCase):
    def test_get_ticker(self):
        try: 
            ticker = self.client.get_ticker('ETHBTC')
            if not good_ticker(ticker):
                self.fail("not a good ticker")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")


class GetTrades(PublicCallsTestCase):
    def test_get_trades_of_all_symbols(self):
        symbols = self.client.get_symbols()
        n_symbols = len(symbols)
        try:
            trades = self.client.get_trades()
            self.assertEqual(len(trades), n_symbols, 'should have trades from all symbols')
            for key in trades:
                trades_of_symbol = trades[key]
                for trade in trades_of_symbol:
                    if not good_public_trade(trade):
                        self.fail("not a good trade")

        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
    
    def test_get_trades_of_many_symbols(self):
        try: 
            trades = self.client.get_trades(['ETHBTC', 'ETHUSD'], limit=2)
            self.assertEqual(len(trades), 2, 'should have trades from only two symbols')
            for key in trades:
                trades_of_symbol = trades[key]
                for trade in trades_of_symbol:
                    if not good_public_trade(trade):
                        self.fail("not a good trade")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

    def test_get_trades_of_one_symbol(self):
        try: 
            trades = self.client.get_trades(['ETHBTC'])
            self.assertEqual(len(trades), 1, 'should have trades from only one symbol')
            for key in trades:
                trades_of_symbol = trades[key]
                for trade in trades_of_symbol:
                    if not good_public_trade(trade):
                        self.fail("not a good trade")
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
    
    def test_asc_sorted(self):
        try:
            trades = self.client.get_trades(sort=args.SORT.ASCENDING)
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
            
    def test_limit_10(self):
        try:
            trades = self.client.get_trades(['ETHBTC'], limit=10)
            self.assertEqual(len(trades['ETHBTC']), 10, 'should have 10 trades')
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")

    def test_offset_10(self):
        try:
            trades = self.client.get_trades(offset=10)
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
    
    def test_since_wrong_format_raise_exception(self):
        with self.assertRaises(CryptomarketSDKException):
            trades = self.client.get_trades(since='yesterday')
    
    def test_since_iso_format(self):
        try:
            iso_datetime = datetime(
                    year=2020, 
                    month=9, 
                    day=19).isoformat()
            trades = self.client.get_trades(since=iso_datetime)
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")
    
    def test_since_id(self):
        try:
            trades = self.client.get_trades(since=1005147907)
        except CryptomarketSDKException as e:
            self.fail("shouldn't raise error")


class GetOrderBooks(PublicCallsTestCase):
    def test_get_all_symbols(self):
        symbols = self.client.get_symbols()
        n_symbols = len(symbols)
        try:
            orderbooks =self.client.get_order_books()
            self.assertEqual(len(orderbooks), n_symbols, "should have one orderbook per symbol")
            for key in orderbooks:
                orderbook_of_symbol = orderbooks[key]
                if not good_orderbook(orderbook_of_symbol):
                    self.fail("not a good orderbook")
        except CryptomarketSDKException as e:
            self.fail("should'n raise error")

    def test_get_many_symbols(self):
        try:
            orderbooks =self.client.get_order_books(symbols=['ETHBTC', 'ETHUSD'], limit=2)
            self.assertEqual(len(orderbooks), 2, "should have two orderbooks")
            for key in orderbooks:
                orderbook_of_symbol = orderbooks[key]
                if not good_orderbook(orderbook_of_symbol):
                    self.fail("not a good orderbook")
        except CryptomarketSDKException as e:
            self.fail("should'n raise error")

    def test_one_symbol(self):
        try:
            orderbooks = self.client.get_order_books(symbols=['ETHBTC'])
            self.assertEqual(len(orderbooks), 1, "should have one orderbook")
            for key in orderbooks:
                orderbook_of_symbol = orderbooks[key]
                if not good_orderbook(orderbook_of_symbol):
                    self.fail("not a good orderbook")
        except CryptomarketSDKException as e:
            self.fail("should'n raise error")
        
class GetOrderBook(PublicCallsTestCase):
    def test_get_orderbook(self):
        try:
            orderbook = self.client.get_order_book(symbol='ETHBTC', limit=2)
            if not good_orderbook(orderbook):
                self.fail("not a good orderbook")
        except CryptomarketSDKException as e:
            self.fail("should'n raise error")

class GetCandles(PublicCallsTestCase):
    def test_get_all_symbols(self):
        symbols = self.client.get_candles()
        n_symbols = len(symbols)
        try:
            candles =self.client.get_candles()
            self.assertEqual(len(candles), n_symbols, "should have one candle per symbol")
            for key in candles:
                candles_of_symbol = candles[key]
                if not good_candle_list(candles_of_symbol):
                    self.fail("not good candles")
        except CryptomarketSDKException as e:
            self.fail("should'n raise error")

    def test_get_many_symbols(self):
        try:
            candles =self.client.get_candles(symbols=['ETHBTC', 'ETHUSD'], limit=2)
            self.assertEqual(len(candles), 2, "should have two candles")
        except CryptomarketSDKException as e:
            self.fail("should'n raise error")

    def test_one_symbol(self):
        try:
            candles = self.client.get_candles(symbols=['ETHBTC'])
            self.assertEqual(len(candles), 1, "should have one candles")
        except CryptomarketSDKException as e:
            self.fail("should'n raise error")

if __name__ == '__main__':
    unittest.main()