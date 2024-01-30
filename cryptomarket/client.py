from dataclasses import asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from dacite import Config, from_dict
from typing_extensions import Literal

import cryptomarket.args as args
from cryptomarket.dataclasses import (Address, AmountLock, Balance, Candle,
                                      Commission, Currency, Order, OrderBook,
                                      Price, PriceHistory, SubAccount, Symbol,
                                      Ticker, Trade, Transaction, Fee)
from cryptomarket.dataclasses.aclSettings import ACLSettings
from cryptomarket.dataclasses.publicTrade import PublicTrade
from cryptomarket.http_client import HttpClient


class Client(object):
    """Cryptomarket rest client.
    :param api_key: The API key
    :param api_secret: The API secret
    :param window: Maximum difference between the creation of the request and the moment of request processing in milliseconds. Max is 60_000. Defaul is 10_000"""

    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, window: Optional[int] = None):
        self.httpClient = HttpClient(api_key, secret_key, window)
        if not api_key is None and not secret_key is None:
            self.httpClient.authorize()

        # aliases of trades
        self.get_trades_by_symbol = self.get_trades_of_symbol
        # aliases of orders
        self.create_new_order = self.create_spot_order
        self.create_spot_order = self.create_spot_order
        self.create_new_spot_order = self.create_spot_order

    def close(self):
        self.httpClient.close_session()

    def _get(self, endpoint: str, params=None):
        return self.httpClient.get(endpoint, params)

    def _post(self, endpoint: str, params=None):
        return self.httpClient.post(endpoint, params)

    def _put(self, endpoint: str, params=None):
        return self.httpClient.put(endpoint, params)

    def _patch(self, endpoint: str, params=None):
        return self.httpClient.patch(endpoint, params)

    def _delete(self, endpoint: str, params=None):
        return self.httpClient.delete(endpoint, params)

    # PUBLIC METHOD CALLS

    def get_currencies(self, currencies: List[str] = None, preferred_network: Optional[str] = None) -> Dict[str, Currency]:
        """Get a dict of all currencies or specified currencies

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#currencies

        :param currencies: Optional. A list of currencies ids
        :param preferred_network: Optional. Code of the default network for currencies

        :returns: A dict of available currencies. indexed by currency id
        """
        params = args.DictBuilder().currencies(
            currencies).preferred_network(preferred_network).build()
        response = self._get(endpoint='public/currency', params=params)
        return {key: from_dict(data_class=Currency, data=response[key])
                for key in response}

    def get_currency(self, currency: str = None) -> Currency:
        """Get the data of a currency

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#currencies

        :param currency: A currency id

        :returns: A currency
        """
        response = self._get(endpoint=f'public/currency/{currency}')
        return from_dict(data_class=Currency, data=response)

    def get_symbols(self, symbols: List[str] = None) -> Dict[str, Symbol]:
        """Get a dict of all symbols or for specified symbols

        A symbol is the combination of the base currency (first one) and quote currency (second one)

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#symbols

        :param symbols: Optional. A list of symbol ids

        :returns: A dict of symbols traded on the exchange, indexed by symbol id
        """
        params = args.DictBuilder().symbols(symbols).build()
        response = self._get(endpoint='public/symbol/', params=params)
        return {key: from_dict(
            data_class=Symbol,
            data=response[key],
            config=Config(cast=[Enum]))
            for key in response}

    def get_symbol(self, symbol: str) -> Symbol:
        """Get a symbol by its id

        A symbol is the combination of the base currency (first one) and quote currency (second one)

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#symbols

        :param symbol: A symbol id

        :returns: A symbol traded on the exchange
        """
        response = self._get(endpoint=f'public/symbol/{symbol}')
        return from_dict(data_class=Symbol, data=response, config=Config(cast=[Enum]))

    def get_tickers(self, symbols: List[str] = None) -> Dict[str, Ticker]:
        """Get a dict of tickers for all symbols or for specified symbols

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#tickers

        :param symbols: Optional. A list of symbol ids

        :returns: A dict of symbols traded on the exchange, indexed by symbol id
        """
        params = args.DictBuilder().symbols(symbols).build()
        response = self._get(endpoint='public/ticker/', params=params)
        return {key: from_dict(data_class=Ticker, data=response[key])
                for key in response}

    def get_ticker(self, symbol: str) -> Ticker:
        """Get the ticker of a symbol

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#tickers

        :param symbol: A symbol id

        :returns: A symbol traded on the exchange
        """
        response = self._get(endpoint=f'public/ticker/{symbol}')
        return from_dict(data_class=Ticker, data=response)

    def get_prices(self, to: str, source: str = None) -> Dict[str, Price]:
        """Get a dict of quotation prices of currencies

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#prices

        :param to: Target currency code
        :param source: Optional. Source currency rate

        :returns: A dict of quotation prices of currencies, indexed by source currency code
        """
        params = args.DictBuilder().from_(source).to(to).build()
        response = self._get(
            endpoint=f'public/price/rate',
            params=params
        )
        return {key: from_dict(data_class=Price, data=response[key])
                for key in response}

    def get_prices_history(
        self,
        to: str,
        source: str = None,
        since: str = None,
        until: str = None,
        period: Optional[Union[
            args.Period, Literal[
                'M1', 'M3', 'M15', 'M30', 'H1', 'H4', 'D1', 'D7', '1M'
            ]
        ]] = None,
        sort: Optional[Union[args.Sort, Literal['ASC', 'DESC']]] = None,
        limit: int = None
    ) -> Dict[str, PriceHistory]:
        """Get quotation prices history

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#prices

        :param to: Target currency code
        :param source: Optional. Source currency rate
        :param period: Optional. A valid tick interval. 'M1' (one minute), 'M3', 'M5', 'M15', 'M30', 'H1' (one hour), 'H4', 'D1' (one day), 'D7', '1M' (one month). Default is 'M30'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param since: Optional. Initial value of the queried interval
        :param until: Optional. Last value of the queried interval
        :param limit: Optional. Prices per currency pair. Defaul is 1. Min is 1. Max is 1000

        :returns: A dict of quotation prices of currencies, indexed by source currency code
        """
        params = args.DictBuilder().from_(source).to(to).since(since).until(
            until).period(period).sort(sort).limit(limit).build()
        response = self._get(
            endpoint=f'public/price/history', params=params)
        return {key: from_dict(data_class=PriceHistory, data=response[key])
                for key in response}

    def get_ticker_last_prices(self, symbols: List[str] = None) -> Dict[str, Price]:
        """Get a dict of the ticker's last prices for all symbols or for the specified symbols

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#prices

        :param symbols: Optional. A list of symbol ids

        :returns: A dict of ticker prices of currencies, indexed by symbol
        """
        params = args.DictBuilder().symbols(symbols).build()
        response = self._get(
            endpoint=f'public/price/ticker', params=params)
        return {key: from_dict(data_class=Price, data=response[key])
                for key in response}

    def get_ticker_last_price_of_symbol(self, symbol: str) -> Price:
        """Get ticker's last prices of a symbol

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#prices

        :param symbol: A symbol id

        :returns: The ticker's last price of a symbol
        """
        response = self._get(endpoint=f'public/price/ticker/{symbol}')
        return from_dict(data_class=Price, data=response)

    def get_trades(
        self,
        symbols: List[str] = None,
        sort_by: Optional[Union[args.SortBy,
                                Literal['id', 'timestamp']]] = None,
        sort: Optional[Union[args.Sort, Literal['ASC', 'DESC']]] = None,
        since: str = None,
        till: str = None,
        limit: int = None
    ) -> Dict[str, List[PublicTrade]]:
        """Get a dict of trades for all symbols or for specified symbols

        'from' param and 'till' param must have the same format, both id or both timestamp

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#trades

        :param symbols: Optional. A list of symbol ids
        :param sort_by: Optional. Sorting parameter. 'id' or 'timestamp'. Default is 'timestamp'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param since: Optional. Initial value of the queried interval
        :param until: Optional. Last value of the queried interval
        :param limit: Optional. Prices per currency pair. Defaul is 10. Min is 1. Max is 1000

        :returns: A dict with a list of trades for each symbol of the query. Indexed by symbol
        """
        params = args.DictBuilder().symbols(symbols).sort(sort).by(
            sort_by).since(since).till(till).limit(limit).build()
        response = self._get(endpoint='public/trades', params=params)
        return {key: [from_dict(data_class=PublicTrade, data=trade_data)
                      for trade_data in response[key]]
                for key in response}

    def get_trades_of_symbol(
        self,
        symbol: str,
        sort_by: Optional[Union[args.SortBy,
                                Literal['id', 'timestamp']]] = None,
        sort: Optional[Union[args.Sort, Literal['ASC', 'DESC']]] = None,
        since: str = None,
        till: str = None,
        limit: int = None,
        offset: int = None
    ) -> List[PublicTrade]:
        """Get trades of a symbol

        'from' param and 'till' param must have the same format, both id or both timestamp

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#trades

        :param symbol: A symbol id
        :param sort_by: Optional. Sorting parameter. 'id' or 'timestamp'. Default is 'timestamp'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param since: Optional. Initial value of the queried interval
        :param until: Optional. Last value of the queried interval
        :param limit: Optional. Prices per currency pair. Defaul is 10. Min is 1. Max is 1000
        :param offset: Optional. Default is 0. Min is 0. Max is 100000

        :returns: A list of trades of the symbol
        """
        params = args.DictBuilder().sort(sort).by(sort_by).since(
            since).till(till).limit(limit).offset(offset).build()
        response = self._get(
            endpoint=f"public/trades/{symbol}", params=params)
        return [from_dict(data_class=PublicTrade, data=trade_data)
                for trade_data in response]

    def get_order_books(
        self,
        symbols: List[str] = None,
        depth: int = None
    ) -> Dict[str, OrderBook]:
        """Get a dict of orderbooks for all symbols or for the specified symbols

        An Order Book is an electronic list of buy and sell orders for a specific symbol, structured by price level

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#order-books

        :param symbols: Optional. A list of symbol ids
        :param depth: Optional. Order Book depth. Default value is 100. Set to 0 to view the full Order Book

        :returns: A dict with the order book for each queried symbol. indexed by symbol
        """
        params = args.DictBuilder().symbols(symbols).depth(depth).build()
        response = self._get(endpoint='public/orderbook', params=params)
        return {key: OrderBook.from_dict(response[key]) for key in response}

    def get_order_book_of_symbol(
        self,
        symbol: str,
        depth: int = None
    ) -> OrderBook:
        """Get order book of a symbol

        An Order Book is an electronic list of buy and sell orders for a specific symbol, structured by price level

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#order-books

        :param symbol: A symbol id
        :param depth: Optional. Order Book depth. Default value is 100. Set to 0 to view the full Order Book

        :returns: The order book of the symbol
        """
        params = args.DictBuilder().depth(depth).build()
        response = self._get(
            endpoint=f'public/orderbook/{symbol}', params=params)
        return OrderBook.from_dict(response)

    def get_order_book_volume_of_symbol(
        self,
        symbol: str,
        volume: int = None
    ) -> Dict[str, Any]:
        """Get order book of a symbol with the desired volume for market depth search

        An Order Book is an electronic list of buy and sell orders for a specific symbol, structured by price level

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#order-books

        :param symbol: A symbol id
        :param volume: Optional. Desired volume for market depth search

        :returns: The order book of the symbol
        """
        params = args.DictBuilder().volume(volume).build()
        response = self._get(
            endpoint=f'public/orderbook/{symbol}', params=params)
        return OrderBook.from_dict(response)

    def get_candles(
        self,
        symbols: List[str] = None,
        period: Optional[Union[
            args.Period, Literal[
                'M1', 'M3', 'M15', 'M30', 'H1', 'H4', 'D1', 'D7', '1M'
            ]
        ]] = None,
        sort: Optional[Union[args.Sort, Literal['ASC', 'DESC']]] = None,
        since: str = None,
        till: str = None,
        limit: int = None
    ) -> Dict[str, List[Candle]]:
        """Get a dict of candles for all symbols or for specified symbols

        Candels are used for OHLC representation

        The result contains candles with non-zero volume only (no trades = no candles)

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#candles

        :param symbol: A symbol id
        :param period: Optional. A valid tick interval. 'M1' (one minute), 'M3', 'M5', 'M15', 'M30', 'H1' (one hour), 'H4', 'D1' (one day), 'D7', '1M' (one month). Default is 'M30'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param from: Optional. Initial value of the queried interval. As DateTime
        :param till: Optional. Last value of the queried interval. As DateTime
        :param limit: Optional. Prices per currency pair. Defaul is 10. Min is 1. Max is 1000

        :returns: A dict with a list of candles for each symbol of the query. indexed by symbol
        """
        params = args.DictBuilder().symbols(symbols).period(period).sort(
            sort).since(since).till(till).limit(limit).build()
        response = self._get(endpoint='public/candles/', params=params)
        return {key: [from_dict(data_class=Candle, data=candle_data)
                      for candle_data in response[key]]
                for key in response}

    def get_candles_of_symbol(
        self,
        symbol: str,
        period: Optional[Union[
            args.Period, Literal[
                'M1', 'M3', 'M15', 'M30', 'H1', 'H4', 'D1', 'D7', '1M'
            ]
        ]] = None,
        sort: Optional[Union[args.Sort, Literal['ASC', 'DESC']]] = None,
        since: str = None,
        till: str = None,
        limit: int = None,
        offset: int = None
    ) -> List[Candle]:
        """Get candles of a symbol

        Candels are used for OHLC representation

        The result contains candles with non-zero volume only (no trades = no candles)

        Requires no API key Access Rights

        https://api.exchange.cryptomkt.com/#candles

        :param symbol: A symbol id
        :param period: Optional. A valid tick interval. 'M1' (one minute), 'M3', 'M5', 'M15', 'M30', 'H1' (one hour), 'H4', 'D1' (one day), 'D7', '1M' (one month). Default is 'M30'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param from: Optional. Initial value of the queried interval. As DateTime
        :param till: Optional. Last value of the queried interval. As DateTime
        :param limit: Optional. Prices per currency pair. Defaul is 100. Min is 1. Max is 1000
        :param offset: Optional. Default is 0. Min is 0. Max is 100000

        :returns: A list of candles of a symbol
        """
        params = args.DictBuilder().period(period).sort(sort).since(
            since).till(till).limit(limit).offset(offset).build()
        response = self._get(
            endpoint=f"public/candles/{symbol}", params=params)
        return [from_dict(data_class=Candle, data=candle_data)
                for candle_data in response]

    #################
    # AUTHENTICATED #
    #################

    ###########
    # TRADING #
    ###########

    def get_spot_trading_balances(self) -> List[Balance]:
        """Get the user's spot trading balance for all currencies with balance

        Requires the "Orderbook, History, Trading balance" API key Access Right

        https://api.exchange.cryptomkt.com/#get-spot-trading-balance


        :returns: A list of spot trading balances
        """
        response = self._get(endpoint='spot/balance')
        return [from_dict(data_class=Balance, data=balance_data)
                for balance_data in response]

    def get_spot_trading_balance_of_currency(self, currency: str) -> Balance:
        """Get the user spot trading balance of a currency

        Requires the "Orderbook, History, Trading balance" API key Access Right

        https://api.exchange.cryptomkt.com/#get-spot-trading-balance

        :param currency: The currency code to query the balance

        :returns: the spot trading balance of a currency
        """
        response = self._get(endpoint=f'spot/balance/{currency}')
        return from_dict(data_class=Balance, data=response)

    def get_all_active_spot_orders(self, symbol: str = None) -> List[Order]:
        """Get the user's active spot orders

        Requires the "Place/cancel orders" API key Access Right

        https://api.exchange.cryptomkt.com/#get-all-active-spot-orders

        :param symbol: Optional. A symbol for filtering the active spot orders

        :returns: A list of orders
        """
        params = args.DictBuilder().symbol(symbol).build()
        response = self._get(endpoint='spot/order', params=params)
        return [from_dict(data_class=Order, data=data, config=Config(cast=[Enum]))
                for data in response]

    def get_active_spot_order(self, client_order_id: str) -> Order:
        """Get an active spot order by its client order id

        Requires the "Place/cancel orders" API key Access Right

        https://api.exchange.cryptomkt.com/#get-active-spot-orders

        :param client order id: The client order id of the order

        :returns: A spot order of the account
        """
        response = self._get(endpoint=f'spot/order/{client_order_id}')
        return from_dict(data_class=Order, data=response, config=Config(cast=[Enum]))

    def create_spot_order(
        self,
        symbol: str,
        side: Union[args.Side, Literal['buy', 'sell']],
        quantity: str,
        type: Optional[Union[args.OrderType, Literal[
            'limit', 'market', 'stopLimit', 'stopMarket', 'takeProfitLimit', 'takeProfitMarket'
        ]]] = None,
        time_in_force: Optional[Union[args.TimeInForce, Literal[
            'GTC', 'IOC', 'FOK', 'Day', 'GTD'
        ]]] = None,
        client_order_id: str = None,
        price: str = None,
        stop_price: str = None,
        expire_time: str = None,
        strict_validate: bool = None,
        post_only: bool = None,
        take_rate: str = None,
        make_rate: str = None
    ) -> Order:
        """Creates a new spot order

        For fee, for price accuracy and quantity, and for order status information see the api docs

        Requires the "Place/cancel orders" API key Access Right

        https://api.exchange.cryptomkt.com/#create-new-spot-order

        :param symbol: Trading symbol
        :param side: Either 'buy' or 'sell'
        :param quantity: Order quantity
        :param client order id: Optional. If given must be unique within the trading day, including all active orders. If not given, is generated by the server
        :param type: Optional. 'limit', 'market', 'stopLimit', 'stopMarket', 'takeProfitLimit' or 'takeProfitMarket'. Default is 'limit'
        :param time in force: Optional. 'GTC', 'IOC', 'FOK', 'Day', 'GTD'. Default to 'GTC'
        :param price: Optional. Required for 'limit' and 'stopLimit'. limit price of the order
        :param stop price: Optional. Required for 'stopLimit' and 'stopMarket' orders. stop price of the order
        :param expire time: Optional. Required for orders with timeInForce = GDT
        :param strict validate: Optional. If False, the server rounds half down for tickerSize and quantityIncrement. Example of ETHBTC: tickSize = '0.000001', then price '0.046016' is valid, '0.0460165' is invalid
        :param post only: Optional. If True, your post_only order causes a match with a pre-existing order as a taker, then the order will be cancelled
        :param take rate: Optional. Liquidity taker fee, a fraction of order volume, such as 0.001 (for 0.1% fee). Can only increase the fee. Used for fee markup.
        :param make rate: Optional. Liquidity provider fee, a fraction of order volume, such as 0.001 (for 0.1% fee). Can only increase the fee. Used for fee markup.

        :returns: A new spot order
        """
        builder = args.DictBuilder().client_order_id(client_order_id).symbol(symbol).side(
            side).quantity(quantity).order_type(type).price(price).stop_price(stop_price)
        params = builder.time_in_force(time_in_force).expire_time(expire_time).strict_validate(
            strict_validate).post_only(post_only).take_rate(take_rate).make_rate(make_rate).build()
        response = self._post(endpoint='spot/order', params=params)
        return from_dict(data_class=Order, data=response, config=Config(cast=[Enum]))

    def create_spot_order_list(
        self,
        contingency_type: Union[args.ContingencyType, Literal['allOrNone', 'oneCancelOther', 'oneTriggerOneCancelOther']],
        orders: List[args.OrderRequest],
        order_list_id: Optional[str] = None,
    ) -> List[Order]:
        """creates a list of spot orders

        Types or Contingency:
        - ContingencyType.ALL_OR_NONE (ContingencyType.AON)
        - ContingencyType.ONE_CANCEL_OTHER (ContingencyType.OCO)
        - ContingencyType.ONE_TRIGGER_OTHER (ContingencyType.OTO)
        - ContingencyType.ONE_TRIGGER_ONE_CANCEL_OTHER (ContingencyType.OTOCO)

        Restriction in the number of orders:
        - An AON list must have 2 or 3 orders
        - An OCO list must have 2 or 3 orders, and only one can be a limit order
        - An OTO list must have 2 or 3 orders
        - An OTOCO must have 3 or 4 orders, and for the secondary only one can be a limit order

        Symbol restrictions:
        - For an AON order list, the symbol code of orders must be unique for each order in the list.
        - For an OCO order list, there are no symbol code restrictions.
        - For an OTO order list, there are no symbol code restrictions.
        - For an OTOCO order list, the symbol code of orders must be the same for all orders in the list (placing orders in different order books is not supported).

        OrderType restrictions:
        - For an AON order list, orders must be OrderType.LIMIT or OrderType.MARKET
        - For an OCO order list, orders must be OrderType.LIMIT, OrderType.STOP_LIMIT, OrderType.STOP_MARKET, OrderType.TAKE_PROFIT_LIMIT or OrderType.TAKE_PROFIT_MARKET.
        - An OCO order list cannot include more than one limit order (the same
        applies to secondary orders in an OTOCO order list).
        - For an OTO order list, there are no order type resctrictions.
        - For an OTOCO order list, the first order must be OrderType.LIMIT, OrderType.MARKET, OrderType.STOP_LIMIT, OrderType.STOP_MARKET, OrderType.TAKE_PROFIT_LIMIT or OrderType.TAKE_PROFIT_MARKET.
        - For an OTOCO order list, the secondary orders have the same restrictions as an OCO order
        - Default is OrderType.LIMIT

        TimeInForce restrictions:
        - For an AON order list, required and must be FOK
        - For an OCO order list is optional, orders can be GTC, IOC (except limit orders), FOK (except limit orders), DAY or GTD
        - For an OTOCO order list, the first order can be GTC, IOC, FOK, DAY, GTD
        - For an OTOCO order list is optional, the secondary orders can be orders must be GTC, IOC (except limit orders), FOK (except limit orders), DAY or GTD

        https://api.exchange.cryptomkt.com/#create-new-spot-order-list

        :param contingency_type: order list type.
        :param orders: the list of orders
        :param order_list_id: order list identifier. If not provided, it will be generated by the system. Must be equal to the client order id of the first order in the request

        :returns: the list of the created orders
        """
        params = args.DictBuilder().contingency_type(contingency_type).orders(
            orders).order_list_id(order_list_id).build()
        response = self._post(endpoint='spot/order/list', params=params)
        return [from_dict(data_class=Order, data=data, config=Config(cast=[Enum]))
                for data in response]

    def replace_spot_order(
        self,
        client_order_id: str,
        new_client_order_id: str,
        quantity: str,
        price: str = None,
        strict_validate: bool = None
    ) -> Order:
        """Replaces a spot order

        For fee, for price accuracy and quantity, and for order status information see the api docs

        Requires the "Place/cancel orders" API key Access Right

        https://api.exchange.cryptomkt.com/#replace-spot-order

        :param client order id: client order id of the old order
        :param new client order id: client order id for the new order
        :param quantity: Order quantity
        :param strict validate: Price and quantity will be checked for incrementation within the symbol’s tick size and quantity step. See the symbol's tick_size and quantity_increment
        :param price: Required if order type is 'limit', 'stopLimit', or 'takeProfitLimit'. Order price

        :returns: The new spot order
        """
        params = args.DictBuilder().new_client_order_id(new_client_order_id).quantity(
            quantity).price(price).strict_validate(strict_validate).build()
        response = self._patch(
            endpoint=f'spot/order/{client_order_id}', params=params)
        return from_dict(data_class=Order, data=response, config=Config(cast=[Enum]))

    def cancel_all_orders(self, symbol: str = None) -> List[Order]:
        """Cancel all active spot orders, or all active orders for a specified symbol

        Requires the "Place/cancel orders" API key Access Right

        https://api.exchange.cryptomkt.com/#cancel-all-spot-orders


        :returns: A list with the canceled spot order
        """
        params = args.DictBuilder().symbol(symbol).build()
        response = self._delete(endpoint='spot/order', params=params)
        return [from_dict(data_class=Order, data=data, config=Config(cast=[Enum]))
                for data in response]

    def cancel_spot_order(self, client_order_id: str) -> Dict[str, Any]:
        """Cancel the order with the client order id

        Requires the "Place/cancel orders" API key Access Right

        https://api.exchange.cryptomkt.com/#cancel-spot-order

        :param client order id: client order id of the order to cancel

        :returns: The canceled spot order
        """
        response = self._delete(endpoint=f'spot/order/{client_order_id}')
        return from_dict(data_class=Order, data=response, config=Config(cast=[Enum]))

    def get_all_trading_commissions(self) -> List[Commission]:
        """Get the personal trading commission rates for all symbols

        Requires the "Place/cancel orders" API key Access Right

        https://api.exchange.cryptomkt.com/#get-all-trading-commission


        :returns: A list of commission rates
        """
        response = self._get(endpoint='spot/fee')
        return [from_dict(data_class=Commission, data=data) for data in response]

    def get_trading_commission(self, symbol: str) -> Commission:
        """Get the personal trading commission rate of a symbol

        Requires the "Place/cancel orders" API key Access Right

        https://api.exchange.cryptomkt.com/#get-trading-commission

        :param symbol: The symbol of the commission rate

        :returns: The commission rate of a symbol
        """
        response = self._get(endpoint=f'spot/fee/{symbol}')
        return from_dict(data_class=Commission, data=response)

    ###################
    # TRADING HISTORY #
    ###################

    def get_spot_orders_history(
        self,
        symbols: List[str] = None,
        sort_by: Union[args.SortBy, Literal['id', 'timestamp']] = None,
        sort: Union[args.Sort, Literal['ASC', 'DESC']] = None,
        since: str = None,
        till: str = None,
        limit: int = None,
        offset: int = None
    ) -> List[Order]:
        """Get all the spot orders

        Orders without executions are deleted after 24 hours

        'from' param and 'till' param must have the same format, both id or both timestamp

        Requires the "Orderbook, History, Trading balance" API key Access Right

        https://api.exchange.cryptomkt.com/#spot-orders-history

        :param symbol: Optional. Filter orders by symbol
        :param sort_by: Optional. Sorting parameter. 'id' or 'timestamp'. Default is 'timestamp'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param from: Optional. Initial value of the queried interval
        :param till: Optional. Last value of the queried interval
        :param limit: Optional. Prices per currency pair. Defaul is 100. Max is 1000
        :param offset: Optional. Default is 0. Max is 100000

        :returns: A list of orders
        """
        params = args.DictBuilder().symbols(symbols).sort(sort).by(
            sort_by).since(since).till(till).limit(limit).offset(offset).build()
        response = self._get(endpoint='spot/history/order', params=params)
        return [from_dict(data_class=Order, data=data, config=Config(cast=[Enum]))
                for data in response]

    def get_spot_trades_history(
        self,
        order_id: str = None,
        symbol: str = None,
        sort_by: Union[args.SortBy, Literal['id', 'timestamp']] = None,
        sort: Union[args.Sort, Literal['ASC', 'DESC']] = None,
        since: str = None,
        till: str = None,
        limit: int = None,
        offset: int = None
    ) -> List[Trade]:
        """Get the user's spot trading history

        Requires the "Orderbook, History, Trading balance" API key Access Right

        https://api.exchange.cryptomkt.com/#spot-trades-history

        :param order id: Optional. Order unique identifier as assigned by the exchange
        :param symbol: Optional. Filter orders by symbol
        :param sort_by: Optional. Sorting parameter. 'id' or 'timestamp'. Default is 'timestamp'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param from: Optional. Initial value of the queried interval
        :param till: Optional. Last value of the queried interval
        :param limit: Optional. Prices per currency pair. Defaul is 100. Max is 1000
        :param offset: Optional. Default is 0. Max is 100000

        :returns: A list of trades
        """
        params = args.DictBuilder().order_id(order_id).symbol(symbol).sort(
            sort).by(sort_by).since(since).till(till).limit(limit).offset(offset).build()
        response = self._get(endpoint='spot/history/trade', params=params)
        return [from_dict(data_class=Trade, data=data) for data in response]

    ######################
    # WALLET MANAGEMENT  #
    ######################

    def get_wallet_balances(self) -> List[Balance]:
        """Get the user's wallet balances for all currencies with balance

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#wallet-balance


        :returns: A list of wallet balances
        """
        response = self._get(endpoint='wallet/balance')
        return [from_dict(data_class=Balance, data=data) for data in response]

    def get_wallet_balance_of_currency(self, currency: str = None) -> Balance:
        """Get the user's wallet balance of a currency

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#wallet-balance

        :param currency: The currency code to query the balance

        :returns: The wallet balance of the currency
        """
        response = self._get(endpoint=f'wallet/balance/{currency}')
        return from_dict(data_class=Balance, data=response)

    def get_deposit_crypto_addresses(self) -> List[Address]:
        """Get the current addresses of the user

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#deposit-crypto-address


        :returns: A list of currency addresses
        """
        response = self._get(endpoint=f'wallet/crypto/address')
        return [from_dict(data_class=Address, data=data) for data in response]

    def get_deposit_crypto_address_of_currency(self, currency: str) -> Address:
        """Get the current addresses of a currency of the user

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#deposit-crypto-address

        :param currency: Currency to get the address

        :returns: A currency address
        """
        params = args.DictBuilder().currency(currency).build()
        response = self._get(endpoint='wallet/crypto/address', params=params)
        return [from_dict(data_class=Address, data=data) for data in response][0]

    def create_deposit_crypto_address(self, currency: str) -> Address:
        """Creates a new address for a currency

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#deposit-crypto-address

        :param currency: currency to create a new address

        :returns: The created address for the currency
        """
        params = args.DictBuilder().currency(currency).build()
        response = self._post(
            endpoint=f'wallet/crypto/address', params=params)
        return from_dict(data_class=Address, data=response)

    def last_10_deposit_crypto_address(self, currency: str) -> List[Address]:
        """Get the last 10 unique addresses used for deposit, by currency

        Addresses used a long time ago may be omitted, even if they are among the last 10 unique addresses

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#last-10-deposit-crypto-address

        :param currency: currency to get the list of addresses

        :returns: A list of addresses
        """
        params = args.DictBuilder().currency(currency).build()
        response = self._get(
            endpoint=f'wallet/crypto/address/recent-deposit', params=params)
        return [from_dict(data_class=Address, data=data) for data in response]

    def last_10_withdrawal_crypto_address(self, currency: str) -> List[Address]:
        """Get the last 10 unique addresses used for withdrawals, by currency

        Addresses used a long time ago may be omitted, even if they are among the last 10 unique addresses

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#last-10-withdrawal-crypto-addresses

        :param currency: currency to get the list of addresses

        :returns: A list of addresses
        """
        params = args.DictBuilder().currency(currency).build()
        response = self._get(
            endpoint=f'wallet/crypto/address/recent-withdraw', params=params)
        return [from_dict(data_class=Address, data=data) for data in response]

    def withdraw_crypto(
        self,
        currency: str,
        amount: str,
        address: str,
        payment_id: str = None,
        include_fee: bool = None,
        auto_commit: bool = None,
        use_offchain: Literal['never', 'optionaly', 'required'] = None,
        public_comment: str = None
    ) -> str:
        """Please take note that changing security settings affects withdrawals:

        - It is impossible to withdraw funds without enabling the two-factor authentication (2FA)

        - Password reset blocks withdrawals for 72 hours

        - Each time a new address is added to the whitelist, it takes 48 hours before that address becomes active for withdrawal

        Successful response to the request does not necessarily mean the resulting transaction got executed immediately. It has to be processed first and may eventually be rolled back

        To see whether a transaction has been finalized call :py:func:`.Client.get_transaction`

        Requires the "Withdraw cryptocurrencies" API key Access Right

        https://api.exchange.cryptomkt.com/#withdraw-crypto

        :param currency: currency code of the crypto to withdraw
        :param amount: amount to be sent to the specified address
        :param address: address identifier
        :param payment_id: Optional.
        :param include_fee: Optional. If true then the amount includes fees. Default is false
        :param auto_commit: Optional. If false then you should commit or rollback the transaction in an hour. Used in two phase commit schema. Default is true
        :param use_offchain: Optional. Whether the withdrawal may be comitted offchain. Accepted values are 'never', 'optionaly' and 'required'. Default is TODO
        :param public_comment: Optional. Maximum lenght is 255

        :returns: The transaction id
        """
        params = args.DictBuilder().currency(currency).address(address).amount(amount).use_offchain(use_offchain).payment_id(
            payment_id).include_fee(include_fee).auto_commit(auto_commit).public_comment(public_comment).build()
        return self._post(endpoint='wallet/crypto/withdraw', params=params)['id']

    def withdraw_crypto_commit(self, id: str) -> bool:
        """Commit a withdrawal

        Requires the "Withdraw cryptocurrencies" API key Access Right

        https://api.exchange.cryptomkt.com/#withdraw-crypto-commit-or-rollback

        :param id: the withdrawal transaction identifier

        :returns: The transaction result. true if the commit is successful
        """
        return self._put(endpoint=f'wallet/crypto/withdraw/{id}')['result']

    def withdraw_crypto_rollback(self, id: str) -> bool:
        """Rollback a withdrawal

        Requires the "Withdraw cryptocurrencies" API key Access Right

        https://api.exchange.cryptomkt.com/#withdraw-crypto-commit-or-rollback

        :param id: the withdrawal transaction identifier

        :returns: The transaction result. true if the rollback is successful
        """
        return self._delete(endpoint=f'wallet/crypto/withdraw/{id}')['result']

    def get_estimate_withdrawal_fee(self, currency: str, amount: str) -> str:
        """Get an estimate of the withdrawal fee

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#estimate-withdraw-fee

        :param currency: the currency code for withdrawal
        :param amount: the expected withdraw amount

        :returns: The expected fee
        """
        params = args.DictBuilder().amount(amount).currency(currency).build()
        return self._get(endpoint='wallet/crypto/fee/estimate', params=params)['fee']

    def get_estimate_withdrawal_fees(self, fee_requests: List[args.FeeRequest]) -> List[Fee]:
        """Get a list of estimates of withdrawal fees

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#estimate-withdraw-fee

        :returns: A list of expected withdrawal fees
        """
        params = [asdict(fee_request) for fee_request in fee_requests]
        result = self._post(
            endpoint='wallet/crypto/fees/estimate', params=params)
        return [Fee.from_dict(fee_data) for fee_data in result]

    def check_if_crypto_address_belong_to_current_account(self, address: str) -> bool:
        """Check if an address is from this account

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#check-if-crypto-address-belongs-to-current-account

        :param address: address to check

        :returns: True if it is from the current account
        """
        params = args.DictBuilder().address(address).build()
        return self._get(endpoint=f'wallet/crypto/address/check-mine', params=params)['result']

    def convert_between_currencies(
        self,
        from_currency: str,
        to_currency: str,
        amount: str
    ) -> List[str]:
        """Converts between currencies

        Successful response to the request does not necessarily mean the resulting transaction got executed immediately. It has to be processed first and may eventually be rolled back

        To see whether a transaction has been finalized, call getTransaction...#TODO:link the right function

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#convert-between-currencies

        :param from currency: currency code of origin
        :param to currency: currency code of destiny
        :param amount: the amount to be converted

        :returns: A list of transaction identifiers of the convertion
        """
        params = args.DictBuilder().from_currency(from_currency).to_currency(
            to_currency).amount(amount).build()
        return self._post(endpoint='wallet/convert', params=params)['result']

    def transfer_between_wallet_and_exchange(
        self,
        currency: str,
        amount: str,
        source: Union[args.Account, Literal['wallet', 'spot']],
        destination: Union[args.Account, Literal['wallet', 'spot']],
    ) -> str:
        """Transfer funds between account types

        'source' param and 'destination' param must be different account types

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#transfer-between-wallet-and-exchange

        :param currency: currency code for transfering
        :param amount: amount to be transfered
        :param source: transfer source account type. Either 'wallet' or 'spot'
        :param destination: transfer source account type. Either 'wallet' or 'spot'

        :returns: the transaction identifier of the transfer
        """
        params = args.DictBuilder().currency(currency).amount(
            amount).source(source).destination(destination).build()
        return self._post(endpoint='wallet/transfer', params=params)[0]

    def transfer_money_to_another_user(
        self,
        currency: str,
        amount: str,
        identify_by: Union[args.IdentifyBy, Literal['email', 'username']],
        identifier: str
    ) -> Dict[str, str]:
        """Transfer funds to another user

        Requires the "Withdraw cryptocurrencies" API key Access Right

        https://api.exchange.cryptomkt.com/#transfer-money-to-another-user

        :param currency: currency code
        :param amount: amount to be transfered
        :param identify_by: type of identifier. Either 'email' or 'username'
        :param identifier: the email or username of the recieving user

        :returns: the transaction identifier of the transfer
        """
        params = args.DictBuilder().currency(currency).amount(
            amount).identify_by(identify_by).identifier(identifier).build()
        return self._post(endpoint='wallet/internal/withdraw', params=params)['result']

    def get_transaction_history(
        self,
        ids: List[str] = None,
        currencies: List[str] = None,
        types: Optional[List[Union[args.TransactionType, Literal[
            'DEPOSIT', 'WITHDRAW', 'TRANSFER', 'SWAP'
        ]]]] = None,
        subtypes: Optional[List[Union[args.TransactionSubType, Literal[
            'UNCLASSIFIED', 'BLOCKCHAIN', 'AIRDROP', 'AFFILIATE', 'STAKING', 'BUY_CRYPTO', 'OFFCHAIN', 'FIAT', 'SUB_ACCOUNT', 'WALLET_TO_SPOT', 'SPOT_TO_WALLET', 'WALLET_TO_DERIVATIVES', 'DERIVATIVES_TO_WALLET', 'CHAIN_SWITCH_FROM', 'CHAIN_SWITCH_TO', 'INSTANT_EXCHANGE'
        ]]]] = None,
        statuses: List[Union[args.TransactionStatus, Literal[
            'CREATED', 'PENDING', 'FAILED', 'SUCCESS', 'ROLLED_BACK'
        ]]] = None,
        sort_by: Optional[Union[args.SortBy,
                                Literal['created_at', 'id']]] = None,
        sort: Optional[Union[args.Sort, Literal['ASC', 'DESC']]] = None,
        id_from: int = None,
        id_till: int = None,
        since: str = None,
        till: str = None,
        limit: int = None,
        offset: int = None
    ) -> List[Transaction]:
        """Get the transaction history of the account

        Important:

        - The list of supported transaction types may be expanded in future versions

        - Some transaction subtypes are reserved for future use and do not purport to provide any functionality on the platform

        - The list of supported transaction subtypes may be expanded in future versions

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#get-transactions-history

        :param ids: Optional. List of transaction identifiers to query
        :param types: Optional. List of types to query. valid types are: 'DEPOSIT', 'WITHDRAW', 'TRANSFER' and 'SWAP'
        :param subtyes: Optional. List of subtypes to query. valid subtypes are: 'UNCLASSIFIED', 'BLOCKCHAIN', 'AIRDROP', 'AFFILIATE', 'STAKING', 'BUY_CRYPTO', 'OFFCHAIN', 'FIAT', 'SUB_ACCOUNT', 'WALLET_TO_SPOT', 'SPOT_TO_WALLET', 'WALLET_TO_DERIVATIVES', 'DERIVATIVES_TO_WALLET', 'CHAIN_SWITCH_FROM', 'CHAIN_SWITCH_TO' and 'INSTANT_EXCHANGE'
        :param statuses: Optional. List of statuses to query. valid subtypes are: 'CREATED', 'PENDING', 'FAILED', 'SUCCESS' and 'ROLLED_BACK'
        :param sort_by: Optional. sorting parameter.'created_at' or 'id'. Default is 'created_at'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param id_from: Optional. Interval initial value when ordering by id. Min is 0
        :param id_till: Optional. Interval end value when ordering by id. Min is 0
        :param since: Optional. Interval initial value when ordering by 'created_at'. As Datetime
        :param till: Optional. Interval end value when ordering by 'created_at'. As Datetime
        :param limit: Optional. Transactions per query. Defaul is 100. Max is 1000
        :param offset: Optional. Default is 0. Max is 100000

        :returns: A list of transactions
        """
        params = args.DictBuilder().currencies(currencies).transaction_types(types).transaction_subtypes(subtypes).transaction_statuses(statuses).id_from(
            id_from).id_till(id_till).tx_ids(ids).sort_by(sort_by).sort(sort).since(since).till(till).limit(limit).offset(offset).build()
        response = self._get(endpoint='wallet/transactions', params=params)
        return [from_dict(data_class=Transaction, data=data, config=Config(cast=[Enum]))
                for data in response]

    def get_transaction(self, id: str) -> Transaction:
        """Get a transaction by its identifier

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#get-transactions-history

        :param id: The identifier of the transaction

        :returns: A transaction of the account
        """
        response = self._get(endpoint=f'wallet/transactions/{id}')
        return from_dict(data_class=Transaction, data=response, config=Config(cast=[Enum]))

    def check_if_offchain_is_available(
        self,
        currency: str,
        address: str,
        payment_id: str = None
    ) -> bool:
        """get the status of the offchain

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#check-if-offchain-is-available

        :param currency: currency code
        :param address: address identifier
        :param payment id: Optional.

        :returns: True if the offchain is available

        .. code-block:: python
        True
        """
        params = args.DictBuilder().currency(currency).address(
            address).payment_id(payment_id).build()
        return self._post(endpoint='wallet/crypto/check-offchain-available', params=params)

    def get_amount_locks(self, currency, active, limit, offset, since, till) -> List[AmountLock]:
        """Get the list of amount locks

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#get-amount-locks

        :param currency: Optional. Currency code
        :param active: Optional. value showing whether the lock is active
        :param limit: Optional. Dafault is 100. Min is 0. Max is 1000
        :param offset: Optional. Default is 0. Min is 0
        :param from: Optional. Interval initial value. As Datetime
        :param till: Optional. Interval end value. As Datetime

        :returns: A list of locks
        """
        params = args.DictBuilder().currency(currency).active(active).limit(
            limit).offset(offset).since(since).till(till).build()
        response = self._get(endpoint='wallet/amount-locks', params=params)
        return [from_dict(data_class=AmountLock, data=data)
                for data in response]

    ######################
    #    SUBACCOUNTS     #
    ######################

    def get_sub_account_list(self) -> List[SubAccount]:
        """Get the list of sub accounts

        Requires no API key Access Rights. Requires to be authenticated

        https://api.exchange.cryptomkt.com/#get-sub-accounts-list
        """
        response = self._get(endpoint='sub-account')
        return [from_dict(data_class=SubAccount, data=data)
                for data in response["result"]]

    def freeze_sub_accounts(self, sub_account_ids: List[str]) -> bool:
        """Freezes the sub accounts listed.
        A frozen wouldn't be able to:
        - login
        - withdraw funds
        - trade
        - complete pending orders
        - use API keys

        For any sub-account listed, all orders will be canceled and all funds will be transferred form the Trading balance

        Requires no API key Access Rights. Requires to be authenticated

        https://api.exchange.cryptomkt.com/#freeze-sub-account

        :param sub_account_ids: A list of sub account ids. Ids as hexadecimal code

        :returns: A boolean indicating whether the sub accounts where frozen. True if successful
        """
        params = args.DictBuilder().sub_account_ids(sub_account_ids).build()
        return self._post(endpoint='sub-account/freeze', params=params)["result"]

    def activate_sub_accounts(self, sub_account_ids: List[str]):
        """Activates sub accounts listed

        unfreezes sub accounts

        Requres no API key Access Rights. Requires to be authenticated

        https://api.exchange.cryptomkt.com/#activate-sub-account

        :param sub_account_ids: A list of sub account ids. Ids as hexadecimal code

        :returns: A boolean indicating whether the sub accounts where activated. True if successful
        """
        params = args.DictBuilder().sub_account_ids(sub_account_ids).build()
        return self._post(endpoint='sub-account/activate', params=params)["result"]

    def transfer_funds(
        self,
        sub_account_id: str,
        amount: str,
        currency: str,
        type: Union[args.TransferType, Literal['to_sub_account', 'from_sub_account']],
    ) -> str:
        """Transfer funds

        Transfers funds from the super-account to a sub-account or from a sub-account to the super-account

        Requires the "Withdraw cryptocurrencies" API key Access Right

        https://api.exchange.cryptomkt.com/#transfer-funds

        :param sub_account_id: id of the sub-account to transfer with the super-account
        :param amount: amount of funds to transfer
        :param currency: currency of transfer
        :param type: 'to_sub_account' or 'from_sub_account'

        :return: the transaction id
        """
        params = args.DictBuilder().sub_account_id(sub_account_id).amount(
            amount).currency(currency).type(type).build()
        return self._post(endpoint='sub-account/transfer', params=params)['result']

    def get_ACL_settings(self, sub_account_ids: List[str]) -> List[ACLSettings]:
        """Get a list of withdrawal settings for all sub-accounts or for the specified sub-accounts

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#get-acl-settings

        :param sub_account_ids: A list of sub account ids. Ids as hexadecimal code

        :return: A list of ACL settings for subaccounts
        """
        params = args.DictBuilder().sub_account_ids(sub_account_ids).build()
        response = self._get(endpoint='sub-account/acl', params=params)
        return [from_dict(data_class=ACLSettings, data=data)
                for data in response["result"]]

    def change_ACL_settings(self, sub_account_ids: List[str], acl_settings: ACLSettings) -> List[ACLSettings]:
        """Change the ACL settings of sub-accounts

        Disables or enables withdrawals for a sub-account

        Requires the "Payment information" API key Access Right

        https://api.exchange.cryptomkt.com/#change-acl-settings

        :param sub_account_ids: A list of sub-account ids. Ids as hexadecimal code
        :param acl_settgins: the new acl settings for the sub-accounts (id of dataclass ignored)

        :return: A list of acl settings of the changed sub-accounts
        """
        params = args.DictBuilder().sub_account_ids(
            sub_account_ids).acl_settings(acl_settings).build()
        response = self._post(endpoint='sub-account/acl', params=params)
        return [from_dict(data_class=ACLSettings, data=data)
                for data in response["result"]]

    def get_sub_account_balance(self, sub_account_id: str) -> Dict[str, List[Balance]]:
        """Get the non-zero balances of a sub-account

        Report will include the wallet and Trading balances.

        Works independent of account state.

        Requires the "Payment information" API key Access Right.

        https://api.exchange.cryptomkt.com/#get-sub-account-balance

        :param sub_account_id: id of the sub-account to get the balances

        :return: a dict of list of balances, indexes are 'wallet' and 'spot'
        """
        response = self._get(endpoint=f'sub-account/balance/{sub_account_id}')
        return {key: [from_dict(data_class=Balance, data=data)
                      for data in response["result"][key]]
                for key in response["result"]}

    def get_sub_account_crypto_address(self, sub_account_id: str, currency: str) -> str:
        """Get the sub-account crypto address for a currency.

        Requires the "Payment information" API key Access Right.

        https://api.exchange.cryptomkt.com/#get-sub-account-crypto-address

        :param sub_account_id: id of the sub-account to get the crypto address
        :param currency: the currency of the crypto address

        :returns: An Address
        """
        response = self._get(
            endpoint=f'sub-account/crypto/address/{sub_account_id}/{currency}')
        return from_dict(data_class=Address, data=response["result"]["address"])
