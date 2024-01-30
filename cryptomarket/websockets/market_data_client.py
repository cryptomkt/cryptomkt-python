from typing import Callable, Dict, List, Optional, Union

from dacite import from_dict
from typing_extensions import Literal

import cryptomarket.args as args
from cryptomarket.dataclasses.wsCandle import WSCandle
from cryptomarket.dataclasses.wsMiniTicker import WSMiniTicker
from cryptomarket.dataclasses.wsOrderBook import WSOrderBook
from cryptomarket.dataclasses.wsOrderBookTop import WSOrderBookTop
from cryptomarket.dataclasses.wsPriceRate import WSPriceRate
from cryptomarket.dataclasses.wsTicker import WSTicker
from cryptomarket.dataclasses.wsTrade import WSTrade
from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.websockets.client_base import ClientBase

SNAPSHOT = 'snapshot'
UPDATE = 'update'
DATA = 'data'


class MarketDataClient(ClientBase):
    """PublicClient connects via websocket to cryptomarket to get market information of the exchange.

    :param callback: A callable to call with the client once the connection is established. if an error ocurrs is return as the fist parameter of the callback: callback(err, client)
    """

    def __init__(self, on_connect: Optional[Callable] = None, on_error: Optional[Callable] = None, on_close: Optional[Callable] = None):
        super(MarketDataClient, self).__init__(
            "wss://api.exchange.cryptomkt.com/api/3/ws/public",
            on_connect=on_connect,
            on_error=on_error,
            on_close=on_close
        )

    def _handle(self, message):
        if 'ch' in message:
            self._handle_channel_feed(message)
        elif 'method' in message:
            self._handle_notification(message)
        elif 'id' in message:
            self._handle_response(message)

    def _handle_channel_feed(self, message):
        channel = message['ch']
        key = channel
        data_key = ''
        if SNAPSHOT in message:
            data_key = SNAPSHOT
        if UPDATE in message:
            data_key = UPDATE
        if DATA in message:
            data_key = DATA
        data = message[data_key]
        callback = self._callback_cache.get_subscription_callback(key)
        callback(data, data_key)

    def _send_channeled_subscription(
        self,
        channel,
        callback,
        params=None,
        result_callback=None
    ):
        key = channel
        self._callback_cache.save_subscription_callback(key, callback)

        def intercept_result(err, result):
            result_callback(err, result['subscriptions'])
        ID = self._callback_cache.save_callback(intercept_result)
        payload = {
            'method': 'subscribe',
            'ch': channel,
            'params': params,
            'id': ID
        }
        self._ws_manager.send(payload)

    def subscribe_to_trades(
        self,
        callback: Callable[[Dict[str, List[WSTrade]], Literal['snapshot', 'update']], None],
        symbols: Optional[List[str]] = None,
        limit: Optional[int] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """Subscribe to a feed of trades

        subscription is for the specified symbols

        normal subscriptions have one update message per symbol

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#subscribe-to-trades

        :param callback: callable that recieves a dict of trades, indexed by symbol.
        :param symbols: A list of symbol ids to subscribe to
        :param limit: Number of historical entries returned in the first feed. Min is 0. Max is 1000. Default is 0
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        params = args.DictBuilder().symbols_as_list(symbols).limit(limit).build()

        def intercept_feed(feed, feed_type):
            result = dict()
            for key in feed:
                result[key] = [from_dict(data_class=WSTrade, data=data)
                               for data in feed[key]]
            callback(result, feed_type)
        self._send_channeled_subscription(
            channel='trades',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_candles(
        self,
        callback: Callable[[Dict[str, List[WSCandle]], Literal['snapshot', 'update']], None],
        symbols: List[str],
        period: Optional[Union[
            args.Period, Literal[
                'M1', 'M3', 'M15', 'M30', 'H1', 'H4', 'D1', 'D7', '1M'
            ]
        ]] = None,
        limit: Optional[int] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of candles

        subscription is for the specified symbols

        normal subscriptions have one update message per symbol

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#subscribe-to-candles


        :param callback: callable that recieves a dict of candles, indexed by symbol.
        :param symbols: A list of symbol ids to subscribe to
        :param period: Optional. A valid tick interval. 'M1' (one minute), 'M3', 'M5', 'M15', 'M30', 'H1' (one hour), 'H4', 'D1' (one day), 'D7', '1M' (one month). Default is 'M30'
        :param limit: Number of historical entries returned in the first feed. Min is 0. Max is 1000. Default is 0
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        def intercept_feed(feed, feed_type):
            result = dict()
            for key in feed:
                result[key] = [
                    from_dict(data_class=WSCandle, data=data) for data in feed[key]]
            callback(result, feed_type)
        params = args.DictBuilder().symbols_as_list(symbols).limit(limit).build()
        self._send_channeled_subscription(
            channel=f'candles/{period}',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback,
        )

    def subscribe_to_mini_ticker(
        self,
        callback: Callable[[Dict[str, WSMiniTicker]], None],
        speed: Union[args.TickerSpeed, Literal['1s', '3s']],
        symbols: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of mini tickers

        subscription is for all symbols or for the specified symbols

        normal subscriptions have one update message per symbol

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#subscribe-to-mini-ticker


        :param callback: callable that recieves a dict of mini tickers, indexed by symbol.
        :param speed: The speed of the feed. '1s' or '3s'
        :param symbols: Optional. A list of symbol ids to subscribe to. If not provided it subscribes to all symbols
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        if symbols is None:
            symbols = ['*']
        params = args.DictBuilder().symbols_as_list(symbols).build()

        def intercept_feed(feed, feed_type):
            callback({key: from_dict(data_class=WSMiniTicker, data=feed[key])
                      for key in feed})
        self._send_channeled_subscription(
            channel=f'ticker/price/{speed}',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_mini_ticker_in_batch(
        self,
        callback: Callable[[Dict[str, WSMiniTicker]], None],
        speed: Union[args.TickerSpeed, Literal['1s', '3s']],
        symbols: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of mini tickers in batches

        subscription is for all symbols or for the specified symbols

        batch subscriptions have a joined update for all symbols

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#subscribe-to-mini-ticker-in-batches

        :param callback: callable that recieves a dict of mini tickers, indexed by symbol.
        :param speed: The speed of the feed. '1s' or '3s'
        :param symbols: Optional. A list of symbol ids to subscribe to. If not provided it subscribes to all symbols
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        if symbols is None:
            symbols = ['*']
        params = args.DictBuilder().symbols_as_list(symbols).build()

        def intercept_feed(feed, feed_type):
            callback({key: from_dict(data_class=WSMiniTicker, data=feed[key])
                      for key in feed})
        self._send_channeled_subscription(
            channel=f'ticker/price/{speed}/batch',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_ticker(
        self,
        callback: Callable[[Dict[str, WSTicker]], None],
        speed: Union[args.TickerSpeed, Literal['1s', '3s']],
        symbols: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of tickers

        subscription is for all symbols or for the specified symbols

        normal subscriptions have one update message per symbol

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#subscribe-to-ticker


        :param callback: callable that recieves a dict of tickers, indexed by symbol.
        :param speed: The speed of the feed. '1s' (1 second) or '3s' (3 seconds)
        :param symbols: Optional. A list of symbol ids to subscribe to. If not provided it subscribes to all symbols
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        if symbols is None:
            symbols = ['*']
        params = args.DictBuilder().symbols_as_list(symbols).build()

        def intercept_feed(feed, feed_type):
            callback({key: from_dict(data_class=WSTicker, data=feed[key])
                      for key in feed})
        self._send_channeled_subscription(
            channel=f'ticker/{speed}',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_ticker_in_batch(
        self,
        callback: Callable[[Dict[str, WSTicker]], None],
        speed: Union[args.TickerSpeed, Literal['1s', '3s']],
        symbols: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of tickers in batches

        subscription is for all symbols or for the specified symbols

        batch subscriptions have a joined update for all symbols

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#subscribe-to-ticker-in-batches

        :param callback: callable that recieves a dict of tickers, indexed by symbol.
        :param speed: The speed of the feed. '1s' (1 second) or '3s' (3 seconds)
        :param symbols: Optional. A list of symbol ids to subscribe to. If not provided it subscribes to all symbols
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        if symbols is None:
            symbols = ['*']
        params = args.DictBuilder().symbols_as_list(symbols).build()

        def intercept_feed(feed, feed_type):
            callback({key: from_dict(data_class=WSTicker, data=feed[key])
                      for key in feed})
        self._send_channeled_subscription(
            channel=f'ticker/{speed}/batch',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_full_order_book(
        self,
        callback: Callable[[Dict[str, WSOrderBook], Literal['snapshot', 'update']], None],
        symbols: List[str],
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of a full orderbook

        subscription is for the specified symbols

        normal subscriptions have one update message per symbol

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#subscribe-to-full-order-book

        :param callback: callable that recieves a dict of order books, indexed by symbol.
        :param symbols: Optional. A list of symbol ids to subscribe to.
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbol
        """
        params = args.DictBuilder().symbols_as_list(symbols).build()

        def intercept_feed(feed, feed_type):
            callback({key: WSOrderBook.from_dict(feed[key]) for key in feed},
                     feed_type)
        self._send_channeled_subscription(
            channel=f'orderbook/full',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_partial_order_book(
        self,
        callback: Callable[[Dict[str, WSOrderBook]], None],
        depth: Union[args.Depth, Literal['D5', 'D10', 'D20']],
        speed: Union[args.OrderbookSpeed, Literal['100ms', '500ms', '1000ms']],
        symbols: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of a partial orderbook

        subscription is for all symbols or for the specified symbols

        normal subscriptions have one update message per symbol

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#subscribe-to-partial-order-book

        :param callback: callable that recieves a dict of partial order books, indexed by symbol.
        :param depth: The depth of the partial orderbook. 'D5', 'D10' or 'D20'
        :param speed: The speed of the feed. '100ms', '500ms' or '1000ms'
        :param symbols: Optional. A list of symbol ids to subscribe to. If not provided it subscribes to all symbols
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """

        if symbols is None:
            symbols = ['*']
        params = args.DictBuilder().symbols_as_list(
            symbols).depth(depth).speed(speed).build()

        def intercept_feed(feed, feed_type):
            callback({key: WSOrderBook.from_dict(feed[key]) for key in feed})
        self._send_channeled_subscription(
            channel=f'orderbook/{depth}/{speed}',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_partial_order_book_in_batch(
        self,
        callback: Callable[[Dict[str, WSOrderBook]], None],
        depth: Union[args.Depth, Literal['D5', 'D10', 'D20']],
        speed: Union[args.OrderbookSpeed, Literal['100ms', '500ms', '1000ms']],
        symbols: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of a partial orderbook in batches

        subscription is for all symbols or for the specified symbols

        batch subscriptions have a joined update for all symbols

        https://api.exchange.cryptomkt.com/#subscribe-to-partial-order-book-in-batches

        :param callback: callable that recieves a dict of partial order books, indexed by symbol.
        :param speed: The speed of the feed. '100ms', '500ms' or '1000ms'
        :param depth: The depth of the partial orderbook. 'D5', 'D10' or 'D20'
        :param symbols: Optional. A list of symbol ids to subscribe to. If not provided it subscribes to all symbols
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        if symbols is None:
            symbols = ['*']
        params = args.DictBuilder().symbols_as_list(symbols).build()

        def intercept_feed(feed, feed_type):
            callback({key: WSOrderBook.from_dict(feed[key]) for key in feed})
        self._send_channeled_subscription(
            channel=f'orderbook/{depth}/{speed}/batch',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_top_of_book(
        self,
        callback: Callable[[Dict[str, WSOrderBookTop]], None],
        speed: Union[args.OrderbookSpeed, Literal['100ms', '500ms', '1000ms']],
        symbols: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of the top of the orderbook

        subscription is for all symbols or for the specified symbols

        normal subscriptions have one update message per symbol

        https://api.exchange.cryptomkt.com/#subscribe-to-top-of-book

        :param callback: callable that recieves a dict of top of order books, indexed by symbol.
        :param speed: The speed of the feed. '100ms', '500ms' or '1000ms'
        :param symbols: Optional. A list of symbol ids to subscribe to. If not provided it subscribes to all symbols
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        if symbols is None:
            symbols = ['*']
        params = args.DictBuilder().symbols_as_list(symbols).build()

        def intercept_feed(feed, feed_type):
            callback({key: from_dict(data_class=WSOrderBookTop, data=feed[key])
                      for key in feed})
        self._send_channeled_subscription(
            channel=f'orderbook/top/{speed}',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_top_of_book_in_batch(
        self,
        callback: Callable[[Dict[str, WSOrderBookTop]], None],
        speed: Union[args.OrderbookSpeed, Literal['100ms', '500ms', '1000ms']],
        symbols: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of the top of the orderbook in batches

        subscription is for all symbols or for the specified symbols

        batch subscriptions have a joined update for all symbols

        https://api.exchange.cryptomkt.com/#subscribe-to-top-of-book-in-batches

        :param callback: callable that recieves a dict of top of order books, indexed by symbol.
        :param speed: The speed of the feed. '100ms', '500ms' or '1000ms'
        :param symbols: Optional. A list of symbol ids to subscribe to. If not provided it subscribes to all symbols
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed symbols
        """
        if symbols is None:
            symbols = ['*']
        params = args.DictBuilder().symbols_as_list(symbols).build()

        def intercept_feed(feed, feed_type):
            callback({key: from_dict(data_class=WSOrderBookTop, data=feed[key])
                      for key in feed})
        self._send_channeled_subscription(
            channel=f'orderbook/top/{speed}/batch',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )

    def subscribe_to_price_rates(
        self,
        callback: Callable[[Dict[str, WSPriceRate]], None],
        speed: Union[args.PriceRateSpeed, Literal['1s', '3s']],
        target_currency: Optional[str],
        currencies: Optional[List[str]] = None,
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[str], None]], None]] = None,
    ):
        """subscribe to a feed of price rates

        subscription is for all currencies or specified currencies (bases), against a target currency (quote). indexed by currency id (bases)

        https://api.exchange.cryptomkt.com/#subscribe-to-price-rates

        :param callback: callable that recieves a dict of mini tickers, indexed by symbol.
        :param speed: The speed of the feed. '1s' or '3s'
        :param target_currency: quote currency for the price rates
        :param currencies: Optional. A list of currencies ids (as bases) to subscribe to. If not provided it subscribes to all currencies
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of correctly subscribed currencies
        """
        if currencies is None:
            currencies = ['*']
        params = args.DictBuilder().currencies_as_list(currencies).speed(speed).target_currency(target_currency).build()

        def intercept_feed(feed, feed_type):
            callback({key: from_dict(data_class=WSPriceRate, data=feed[key])
                      for key in feed})
        self._send_channeled_subscription(
            channel=f'price/rate/{speed}',
            callback=intercept_feed,
            params=params,
            result_callback=result_callback
        )
