from typing import Any, Dict, List, Union

import cryptomarket.args as args
from cryptomarket.websockets.client_base import ClientBase
from cryptomarket.websockets.orderbook_cache import OrderbookCache


class PublicClient(ClientBase):
    """PublicClient connects via websocket to cryptomarket to get market information of the exchange.

    :param callback: A callable to call with the client once the connection is established. if an error ocurrs is return as the fist parameter of the callback: callback(err, client)
    """
    def __init__(self, on_connect=None, on_error=None, on_close=None):
        super(PublicClient, self).__init__(
            "wss://api.exchange.cryptomkt.com/api/2/ws/public", 
            subscription_keys={
                # tickers
                'subscribeTicker':'tickers',
                'unsubscribeTicker':'tickers',
                'ticker':'tickers',
                # orderbooks
                'subscribeOrderbook':'orderbooks',
                'unsubscribeOrderbook':'orderbooks',
                'snapshotOrderbook':'orderbooks',
                'updateOrderbook':'orderbooks',
                # trades
                'subscribeTrades':'trades',
                'unsubscribeTrades':'trades',
                'snapshotTrades':'trades',
                'updateTrades':'trades',
                # candles
                'subscribeCandles':'candles',
                'unsubscribeCandles':'candles',
                'snapshotCandles':'candles',
                'updateCandles':'candles',
            },
            on_connect=on_connect, 
            on_error=on_error, 
            on_close=on_close
        )
        self.ob_cache = OrderbookCache()
    
    def orderbook_feed(self, method):
        return method == 'snapshotOrderbook' or method == 'updateOrderbook'

    def candles_feed(self, method):
        return method == 'snapshotCandles' or method == 'updateCandles'

    def trades_feed(self, method):
        return method == 'snapshotTrades' or method == 'updateTrades'
    
    def handle_notification(self, message):
        params = message['params']
        method = message['method']
        key = self.build_key(method, params)
        callback = self.callback_cache.get_subscription_callback(key)
        if callback is None: return
        subscription_data = None
        if self.orderbook_feed(method):
            self.ob_cache.update(method, key, params)
            if self.ob_cache.orderbook_broken(key):
                self.send_by_id('subscribeOrderbook', None, {'symbol':symbol})
                self.ob_cache.wait_orderbook(key)
            if self.ob_cache.orderbook_wating(key): return
            subscription_data = self.ob_cache.get_ob(key)

        elif self.trades_feed(method) or self.candles_feed(method):
            subscription_data = params['data']

        else:
            subscription_data = params

        callback(subscription_data)

    def build_key(self, method, params):
        m_key = self.subscription_keys[method]
        symbol = params['symbol'] if 'symbol' in params else ''
        period = params['period'] if 'period' in params else ''
        key = m_key + ':' + symbol + ':' + period
        return key.upper()

    def get_currencies(self, callback: callable):
        """Get a list all available currencies on the exchange.

        https://api.exchange.cryptomkt.com/#get-currencies

        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: A list of all available currencies as result argument for the callback.

        .. code-block:: python
        [
            {
                "id":"BTC",
                "fullName":"Bitcoin",
                "crypto":True,
                "payinEnabled":True,
                "payinPaymentId":False,
                "payinConfirmations":1,
                "payoutEnabled":True,
                "payoutIsPaymentId":False,
                "transferEnabled":True,
                "delisted":False,
                "payoutFee":"0.0003282"
            },
            {
                "id":"ETH",
                "fullName":"Ethereum",
                "crypto":True,
                "payinEnabled":True,
                "payinPaymentId":False,
                "payinConfirmations":9,
                "payoutEnabled":True,
                "payoutIsPaymentId":False,
                "transferEnabled":True,
                "delisted":False,
                "payoutFee":"0.007936507936"
            }
        ]
        """
        self.send_by_id(method='getCurrencies', callback=callback)
    
    def get_currency(self, currency: str, callback: callable):
        """Get the data of a currency.

        https://api.exchange.cryptomkt.com/#get-currencies

        :param currency: A currency id.
        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: A currency as result argument for the callback.

        .. code-block:: python
        {
            'id': 'EOS', 
            'fullName': 'EOS', 
            'crypto': True, 
            'payinEnabled': True, 
            'payinPaymentId': True, 
            'payinConfirmations': 25, 
            'payoutEnabled': True, 
            'payoutIsPaymentId': True, 
            'transferEnabled': True, 
            'delisted': False, 
            'payoutFee': '0.0926'
        }
        """
        params = args.DictBuilder().currency(currency).build()
        self.send_by_id(method='getCurrency', callback=callback, params=params)

    def get_symbols(self, callback: callable):
        """Get a list of the specified symbols or all of them if no symbols are specified.
            
        A symbol is the combination of the base currency (first one) and quote currency (second one).

        https://api.exchange.cryptomkt.com/#get-symbols

        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: A list of currency symbols traded on the exchange as result argument for the callback.

        .. code-block:: python
        {
            "id": "ETHBTC",
            "baseCurrency": "ETH",
            "quoteCurrency": "BTC",
            "quantityIncrement": "0.001",
            "tickSize": "0.000001",
            "takeLiquidityRate": "0.001",
            "provideLiquidityRate": "-0.0001",
            "feeCurrency": "BTC"
        }
        """
        self.send_by_id(method='getSymbols', callback=callback)
    
    def get_symbol(self, symbol: str, callback: callable):
        """Get a symbol by its id.

        A symbol is the combination of the base currency (first one) and quote currency (second one).

        https://api.exchange.cryptomkt.com/#get-symbols

        :param symbol: A symbol id.
        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: A symbol traded on the exchange as result argument for the callback.

        .. code-block:: python
        {
            "id":"EOSETH",
            "baseCurrency":"EOS",
            "quoteCurrency":"ETH",
            "quantityIncrement":"0.01",
            "tickSize":"0.0000001",
            "takeLiquidityRate":"0.002",
            "provideLiquidityRate":"0.001",
            "feeCurrency":"ETH"
        }
        """
        params = args.DictBuilder().symbol(symbol).build()
        self.send_by_id(method='getSymbol', callback=callback, params=params)

    def get_trades(self,
    symbol: str,
    callback: callable,
    sort: str = None,
    by: str = None,
    since: str = None, 
    till: str = None, 
    limit: int = None, 
    offset: int = None):
        """Get trades of the specified symbol.

        https://api.exchange.cryptomkt.com/#get-trades

        :param symbol: The symbol to get the trades.
        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'.
        :param since: Optional. Initial value of the queried interval. As id or as Datetime.
        :param till: Optional. Last value of the queried interval. As id or as Datetime.
        :param limit: Optional. Trades per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 

        :returns: Trades information of the symbol as result argument for the callback.

        .. code-block:: python
        [
            {
                "id":1011897072,
                "price":"0.032338",
                "quantity":"0.0054",
                "side":"sell",
                "timestamp":"2020-11-23T19:13:35.386Z"
            },
            {
                "id":1011897068,
                "price":"0.032340",
                "quantity":"1.0600",
                "side":"buy",
                "timestamp":"2020-11-23T19:13:34.773Z"
            }
        ]
        """
        params = args.DictBuilder().symbol(symbol).sort(sort).by(by).since(since).till(till).limit(limit).offset(offset).build()
        self.send_by_id(method='getTrades', callback=callback, params=params)

    #################
    # subscriptions #
    #################

    def subscribe_to_ticker(self, symbol: str, callback: callable, result_callback: callable=None):
        """Subscribe to a ticker of a symbol.

        https://api.exchange.cryptomkt.com/#subscribe-to-ticker

        :param symbol: A symbol to subscribe.
        :param callback: A callable to call with each update of the result data. It takes one argument, the feed of tickers.
        :param result_callback: A callable to call with the subscription result. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: Tickers of the symbol as feed for the callback.

        .. code-block:: python
        {
            "ask":"0.00017762",
            "bid":"0.00017755",
            "last":"0.00017738",
            "open":"0.0001677",
            "low":"0.00016512",
            "high":"0.00017932",
            "volume":"3164087.05",
            "volumeQuote":"540.9955071082",
            "timestamp":"2020-11-23T18:31:31.465Z",
            "symbol":"EOSBTC"
        }
        """
        params = args.DictBuilder().symbol(symbol).build()
        self.send_subscription(method='subscribeTicker', callback=callback, params=params, result_callback=result_callback)

    def unsubscribe_to_ticker(self, symbol: str, callback: callable=None):
        """Unsubscribe to a ticker of a symbol.

        https://api.exchange.cryptomkt.com/#subscribe-to-ticker

        :param symbol: The symbol to stop the ticker subscribption.
        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The operation result as result argument for the callback. True if success.
        """
        params = args.DictBuilder().symbol(symbol).build()
        self.send_unsubscription(method='unsubscribeTicker', callback=callback, params=params)

    def subscribe_to_order_book(self, symbol: str, callback: callable, result_callback: callable=None):
        """Subscribe to the order book of a symbol.

        An Order Book is an electronic list of buy and sell orders for a specific symbol, structured by price level.

        https://api.exchange.cryptomkt.com/#subscribe-to-order-book

        :param symbol: The symbol of the orderbook.
        :param callback: A callable to call with each update of the result data. It takes one argument, the feed of order book.
        :param result_callback: Optional. A callable to call with the subscription result. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result)

        :returns: Order books of the symbol as feed for the callback.
        """
        params = args.DictBuilder().symbol(symbol).build()
        self.send_subscription(method='subscribeOrderbook', callback=callback, params=params, result_callback=result_callback)

    def unsubscribe_to_order_book(self, symbol: str, callback: callable=None):
        """Unsubscribe to an order book of a symbol.

        An Order Book is an electronic list of buy and sell orders for a specific symbol, structured by price level.

        https://api.exchange.cryptomkt.com/#subscribe-to-order-book

        :param symbol: The symbol of the orderbook.
        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The operation result as result argument for the callback. True if success.
        """
        params = args.DictBuilder().symbol(symbol).build()
        self.send_unsubscription(method='unsubscribeOrderbook', callback=callback, params=params)

    def subscribe_to_trades(self, symbol:str, callback: callable, limit:int=None, result_callback: callable=None):
        """Subscribe to the trades of a symbol.

        https://api.exchange.cryptomkt.com/#subscribe-to-trades

        :param symbol: The symbol of the trades.
        :param callback: A callable to call with each update of the result data. It takes one argument, the feed of trades.
        :param limit: Optional. Maximum number of trades in the feed.
        :param result_callback: Optional. A callable to call with the subscription result. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: A Trade list of the symbol as feed for the callback.

        .. code-block:: python
        [
            {
                "id":1011873515,
                "price":"0.032461",
                "quantity":"0.1000",
                "side":"buy",
                "timestamp":"2020-11-23T18:47:06.046Z"
            },
            {
                "id":1011873516,
                "price":"0.032462",
                "quantity":"0.9143",
                "side":"buy",
                "timestamp":"2020-11-23T18:47:06.046Z"
            }
        ]
        """
        params = args.DictBuilder().symbol(symbol).limit(limit).build()
        self.send_subscription(method='subscribeTrades', callback=callback, params=params, result_callback=result_callback)

    def unsubscribe_to_trades(self, symbol: str, callback: callable= None):
        """Unsubscribe to a trades of a symbol.

        https://api.exchange.cryptomkt.com/#subscribe-to-trades

        :param symbol: The symbol of the trades.
        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The operation result as result argument for the callback. True if success.
        """
        params = args.DictBuilder().symbol(symbol).build()
        self.send_unsubscription(method='unsubscribeTrades', callback=callback, params=params)

    def subscribe_to_candles(self,
    symbol: str, 
    period: str, 
    callback: callable, 
    limit: int = None,
    result_callback: callable=None):
        """Subscribe to the candles of a symbol, at the given period.

        Candels are used for OHLC representation.

        https://api.exchange.cryptomkt.com/#subscribe-to-candles

        :param symbols: A list of symbol ids.
        :param period: A valid tick interval. 'M1' (one minute), 'M3', 'M5', 'M15', 'M30', 'H1' (one hour), 'H4', 'D1' (one day), 'D7', '1M' (one month).
        :param callback: A callable to call with each update of the result data. It takes one argument. The candle feed.
        :param limit: Optional. Maximum number of candles in the feed
        :param result_callback: Optional. A callable to call with the subscription result. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).
        
        :returns: The candle feed of the given symbol and period as feed for the callback.

        .. code-block:: python
        [
            {
                "timestamp":"2020-11-23T19:19:00.000Z",
                "open":"0.032383",
                "close":"0.032382",
                "min":"0.032376",
                "max":"0.032395",
                "volume":"25.5738",
                "volumeQuote":"0.8282975861"
            },
            {
                "timestamp":"2020-11-23T19:20:00.000Z",
                "open":"0.032387",
                "close":"0.032383",
                "min":"0.032374",
                "max":"0.032387",
                "volume":"8.5926",
                "volumeQuote":"0.2782366624"
            }
        ]
        """
        params = args.DictBuilder().symbol(symbol).period(period).limit(limit).build()
        self.send_subscription(method='subscribeCandles', callback=callback, params=params, result_callback=result_callback)
        
    def unsubscribe_to_candles(self, symbol: str, period: str, callback: callable=None):
        """Unsubscribe to the candles of a symbol at a given period.

        https://api.exchange.cryptomkt.com/#subscribe-to-candles

        :param symbol: The symbol of the candles.
        :param period: 'M1' (one minute), 'M3', 'M5', 'M15', 'M30', 'H1' (one hour), 'H4', 'D1' (one day), 'D7', '1M' (one month).
        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The operation result as result argument for the callback. True if success
        """
        params = args.DictBuilder().symbol(symbol).period(period).build()
        self.send_unsubscription(method='unsubscribeCandles', callback=callback, params=params)
