from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import cryptomarket.args as args
from cryptomarket.httpClient import HttpClient


class Client(object):
    def __init__(self, api_key:Optional[str] = None, secret_key:Optional[str] = None):
        self.httpClient = HttpClient(api_key, secret_key)
        self.authed = False
    
    def close(self):
        self.httpClient.close_session()

    def _get(self, endpoint:str, params=None):
        if not self.authed: self.httpClient.authorize()
        return self.httpClient.get(endpoint, params)
    
    def _public_get(self, endpoint:str, params=None):
        return self.httpClient.get(endpoint, params)

    def _post(self, endpoint:str, params=None):
        if not self.authed: self.httpClient.authorize()
        return self.httpClient.post(endpoint, params)

    def _put(self, endpoint:str, params=None):
        if not self.authed: self.httpClient.authorize()
        return self.httpClient.put(endpoint, params)

    def _delete(self, endpoint:str, params=None):
        if not self.authed: self.httpClient.authorize()
        return self.httpClient.delete(endpoint, params)

    # PUBLIC METHOD CALLS

    def get_currencies(self, currencies: List[str] = None) -> List[Dict[str, Any]]:
        """Get a list of all currencies or specified currencies.

        https://api.exchange.cryptomkt.com/#currencies

        :param currencies: Optional. A list of currencies ids.

        :returns: A list of available currencies.

        .. code-block:: python
        [
            {
                "id": "BTC",
                "fullName": "Bitcoin",
                "crypto": true,
                "payinEnabled": true,
                "payinPaymentId": false,
                "payinConfirmations": 2,
                "payoutEnabled": true,
                "payoutIsPaymentId": false,
                "transferEnabled": true,
                "delisted": false,
                "payoutFee": "0.00958",
                "payoutMinimalAmount": "0.00958",
                "precisionPayout": 10,
                "precisionTransfer": 10
            },
            {
                "id": "ETH",
                "fullName": "Ethereum",
                "crypto": true,
                "payinEnabled": true,
                "payinPaymentId": false,
                "payinConfirmations": 2,
                "payoutEnabled": true,
                "payoutIsPaymentId": false,
                "transferEnabled": true,
                "delisted": false,
                "payoutFee": "0.001",
                "payoutMinimalAmount": "0.00958",
                "precisionPayout": 20,
                "precisionTransfer": 15
            }
        ]
        """
        params = args.DictBuilder().currencies(currencies).build()
        return self._public_get(endpoint='public/currency', params=params)
    
    def get_currency(self, currency: str = None) -> Dict[str, Any]:
        """Get the data of a currency.

        https://api.exchange.cryptomkt.com/#currencies

        :param currency: A currency id.

        :returns: A currency.

        .. code-block:: python
        {
            "id": "ETH",
            "fullName": "Ethereum",
            "crypto": true,
            "payinEnabled": true,
            "payinPaymentId": false,
            "payinConfirmations": 20,
            "payoutEnabled": true,
            "payoutIsPaymentId": false,
            "transferEnabled": true,
            "delisted": false,
            "payoutFee": "0.042800000000",
            "payoutMinimalAmount": "0.00958",
            "precisionPayout": 10,
            "precisionTransfer": 10,
        }
        """
        return self._public_get(endpoint=f'public/currency/{currency}')
    
    def get_symbols(self, symbols: List[str] = None) -> List[Dict[str, Any]]:
        """Get a list of all symbols or for specified symbols.
        
        A symbol is the combination of the base currency (first one) and quote currency (second one).

        https://api.exchange.cryptomkt.com/#symbols

        :param symbols: Optional. A list of symbol ids.

        :returns: A list of symbols traded on the exchange.

        .. code-block:: python
        [
            {
                'id': 'ETHEUR', 
                'baseCurrency': 'ETH', 
                'quoteCurrency': 'EUR', 
                'quantityIncrement': '0.01', 
                'tickSize': '0.1', 
                'takeLiquidityRate': '0.002', 
                'provideLiquidityRate': '0.001', 
                'feeCurrency': 'EUR'
            }, 
            {
                'id': 'ETHBTC', 
                'baseCurrency': 
                'ETH', 'quoteCurrency': 'BTC', 
                'quantityIncrement': '0.0001', 
                'tickSize': '0.000001', 
                'takeLiquidityRate': '0.002', 
                'provideLiquidityRate': '0.001', 
                'feeCurrency': 'BTC'
            }
        ]
        """
        params = args.DictBuilder().symbols(symbols).build()
        return self._public_get(endpoint='public/symbol/', params=params)

    def get_symbol(self, symbol: str) -> Dict[str, Any]:
        """Get a symbol by its id.
        
        A symbol is the combination of the base currency (first one) and quote currency (second one).

        https://api.exchange.cryptomkt.com/#symbols

        :param symbol: A symbol id.

        :returns: A symbol traded on the exchange.

        .. code-block:: python
        {
            "id": "ETHBTC",
            "baseCurrency": "ETH",
            "quoteCurrency": "BTC",
            "quantityIncrement": "0.0001",
            "tickSize": "0.000001",
            "takeLiquidityRate": "0.002",
            "provideLiquidityRate": "0.001",
            "feeCurrency": "BTC"
        }
        """
        return self._get(endpoint=f'public/symbol/{symbol}')


    def get_tickers(self, symbols: List[str] = None) -> List[Dict[str, Any]]:
        """Get tickers for all symbols or for specified symbols.            

        :param symbols: Optional. A list of symbol ids.

        :returns: A list of tickers.

        .. code-block:: python
        [
            {
                "symbol":"ETHUSD",
                "ask":"481.246",
                "bid":"481.031",
                "last":"481.090",
                "low":"457.098",
                "high":"484.550",
                "open":"462.287",
                "volume":"178669.5122",
                "volumeQuote":"84162894.0360008",
                "timestamp":"2020-11-17T20:30:05.535Z",
            },
            {
                "symbol":"ETHBTC",
                "ask":"0.027311",
                "bid":"0.027303",
                "last":"0.027303",
                "low":"0.026869",
                "high":"0.027991",
                "open":"0.027476",
                "volume":"49252.6430",
                "volumeQuote":"1360.7600145487",
                "timestamp":"2020-11-17T20:30:05.524Z",
            }
        ]
        """
        params = args.DictBuilder().symbols(symbols).build()
        return self._public_get(endpoint='public/ticker/', params=params)
    
    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get the ticker of a symbol.

        https://api.exchange.cryptomkt.com/#tickers

        :param symbol: A symbol id.

        :returns: The ticker of a symbol.

        .. code-block:: python  
        {
            "symbol":"ETHBTC",
            "ask":"0.027238",
            "bid":"0.027235",
            "last":"0.027260",
            "low":"0.026869",
            "high":"0.027991",
            "open":"0.027506",
            "volume":"49024.5773",
            "volumeQuote":"1354.4721925569",
            "timestamp":"2020-11-17T20:37:00.199Z",
        }
        """
        return self._get(endpoint=f'public/ticker/{symbol}')

    def get_trades(self, 
    symbols: List[str] = None,
    sort: str = None, 
    since: str = None,
    till: str = None, 
    limit: int = None,
    offset: int = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get trades for all symbols or for specified symbols.

        'since' param and 'till' param must have the same format, both index or both timestamp.

        https://api.exchange.cryptomkt.com/#trades

        :param symbols: Optional. A list of symbol ids.
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'.
        :param since: Optional. Initial value of the queried interval. As id or as Datetime.
        :param till: Optional. Last value of the queried interval. As id or as Datetime.
        :param limit: Optional. Trades per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 

        :returns: A list of trades for each symbol of the query.

        .. code-block:: python
        {
            "ETHUSD":[
                {
                    "id":1005147943,
                    "price":"481.617",
                    "quantity":"2.4000",
                    "side":"buy",
                    "timestamp":"2020-11-17T20:49:46.140Z"
                },
                {
                    "id":1005147795,
                    "price":"481.654",
                    "quantity":"0.0005",
                    "side":"buy",
                    "timestamp":"2020-11-17T20:49:32.053Z"
                }
            ],
            "ETHBTC":[
                {
                    "id":1005147904,
                    "price":"0.027275",
                    "quantity":"0.2834",
                    "side":"buy",
                    "timestamp":"2020-11-17T20:49:42.710Z"
                },
                {
                    "id":1005147903,
                    "price":"0.027274",
                    "quantity":"0.3265",
                    "side":"buy",
                    "timestamp":"2020-11-17T20:49:42.710Z"
                }
            ]
        }
        """
        params = args.DictBuilder().symbols(symbols).sort(sort).since(since).till(till).limit(limit).offset(offset).build()
        return self._public_get(endpoint='public/trades/', params=params)

    def get_trades_of_symbol(self,
    symbol: str,
    sort: str = None,
    by: str = None,
    since: str = None,
    till: str = None,
    limit: int = None,
    offset: int = None) -> List[Dict[str, Any]]:
        """Get trades of a symbol.

        'since' param and 'till' param must have the same format, both index or both timestamp.

        https://api.exchange.cryptomkt.com/#trades

        :param symbols: Optional. A list of symbol ids.
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'.
        :param since: Optional. Initial value of the queried interval. As id or as Datetime.
        :param till: Optional. Last value of the queried interval. As id or as Datetime.
        :param limit: Optional. Trades per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 

        :returns: A list of trades of the queried symbol.

        .. code-block:: python
        [
            {
                "id": 9533117,
                "price": "0.046001",
                "quantity": "0.220",
                "side": "sell",
                "timestamp": "2017-04-14T12:18:40.426Z"
            },
            {
                "id": 9533116,
                "price": "0.046002",
                "quantity": "0.022",
                "side": "buy",
                "timestamp": "2017-04-14T11:56:37.027Z"
            }
        ]
        """
        params = args.DictBuilder().sort(sort).by(by).since(since).till(till).limit(limit).offset(offset).build()
        return self._public_get(endpoint=f"public/trades/{symbol}", params=params)

    def get_order_books(self, 
    symbols: List[str] = None,
    limit: int = None) -> Dict[str, Dict[str, Any]]:
        """Get order book for all symbols or for the specified symbols.

        An Order Book is an electronic list of buy and sell orders for a specific symbol, structured by price level.

        https://api.exchange.cryptomkt.com/#order-book

        :param symbols: Optional. A list of symbol ids.
        :param limit: Optional. Limit of order book levels. Set to 0 to view full list of order book levels.

        :returns: The order book for each queried symbol.

        .. code-block:: python
        {
            "ETHUSD":{
                "symbol":"ETHUSD",
                "timestamp":"2020-11-17T22:02:17.617Z",
                "batchingTime":"2020-11-17T22:02:17.628Z",
                "ask":[
                    {
                        "price":"479.844",
                        "size":"2.4000"
                    },
                    {
                        "price":"479.858",
                        "size":"0.4650"
                    }
                ],
                "bid":[
                    {
                        "price":"479.815",
                        "size":"6.2310"
                    },
                    {
                        "price":"479.795",
                        "size":"2.4000"
                    }
                ]
            },
            "ETHBTC":{
                "symbol":"ETHBTC",
                "timestamp":"2020-11-17T22:02:17.611Z",
                "batchingTime":"2020-11-17T22:02:17.627Z",
                "ask":[
                    {
                        "price":"0.027297",
                        "size":"0.6483"
                    },
                    {
                        "price":"0.027298",
                        "size":"5.9372"
                    }
                ],
                "bid":[
                    {
                        "price":"0.027295",
                        "size":"0.9000"
                    },
                    {
                        "price":"0.027294",
                        "size":"0.2831"
                    }
                ]
            }
        }
        """
        params = args.DictBuilder().symbols(symbols).limit(limit).build()
        return self._public_get(endpoint='public/orderbook/', params=params)
    
    def get_order_book(self, 
    symbol: str,
    limit: int = None) -> Dict[str, Any]:
        """Get An order book of a symbols.

        An Order Book is an electronic list of buy and sell orders for a specific symbol, structured by price level.

        https://api.exchange.cryptomkt.com/#order-book

        :param symbol: A symbol id.
        :param limit: Optional. Limit of order book levels. Set to 0 to view full list of order book levels.
        
        :returns: The order book for the symbol.

        .. code-block:: python
        {
            "symbol":"ETHBTC",
            "timestamp":"2020-11-17T22:08:19.426Z",
            "batchingTime":"2020-11-17T22:08:19.440Z",
            "ask":[
                {
                    "price":"0.027288",
                    "size":"0.9000"
                },
                {
                    "price":"0.027292",
                    "size":"0.3265"
                }
            ],
            "bid":[
                {
                    "price":"0.027281",
                    "size":"4.9000"
                },
                {
                    "price":"0.027280",
                    "size":"11.1017"
                }
            ]
        }
        """
        params = args.DictBuilder().limit(limit).build()
        return self._public_get(endpoint=f'public/orderbook/{symbol}', params=params)
    
    def market_depth(self,
    symbol: str,
    volume: int) -> Dict[str, Any]:
        """Get An order book with market depth data of a symbol.

        An Order Book is an electronic list of buy and sell orders for a specific symbol, structured by price level.

        https://api.exchange.cryptomkt.com/#order-book

        :param symbol: A symbol id.
        :param volume: Optional. Desired volume for market depth search

        :returns: The order book for the symbol with market depth data.

        .. code-block:: python
        {
            "ask": [
                {
                "price": "9779.68",
                "size": "2.497"
                }
            ],
            "bid": [
                {
                "price": "9779.67",
                "size": "0.03719"
                },
                {
                "price": "9779.29",
                "size": "0.171"
                },
                {
                "price": "9779.27",
                "size": "0.171"
                },
                {
                "price": "9779.21",
                "size": "0.171"
                }
            ],
            "timestamp": "2020-02-11T11:30:38.597950917Z",
            "askAveragePrice": "9779.68",
            "bidAveragePrice": "9779.29"
        }
        """
        params = args.DictBuilder().volume(volume).build()
        return self._public_get(endpoint=f'public/orderbook/{symbol}', params=params)


    def get_candles(self, 
    symbols: List[str] = None,
    period: str = None,
    sort: str = None,
    since: str = None,
    till: str = None, 
    limit: int = None,
    offset: int = None) -> Dict[str, List[Dict[str, List[Dict[str, Any]]]]]:
        """Get candles for all symbols or for specified symbols.

        Candels are used for OHLC representation.

        https://api.exchange.cryptomkt.com/#candles

        :param symbols: Optional. A list of symbol ids.
        :param period: Optional. A valid tick interval. 'M1' (one minute), 'M3', 'M5', 'M15', 'M30', 'H1' (one hour), 'H4', 'D1' (one day), 'D7', '1M' (one month). Default is 'M30'.
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'.
        :param since: Optional. Initial value of the queried interval.
        :param till: Optional. Last value of the queried interval.
        :param limit: Optional. Candles per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 

        :returns: The candles for each queried symbol.

        .. code-block:: python
        {
            "ETHUSD":[
                {
                    "timestamp":"2017-05-05T15:00:00.000Z",
                    "open":"10",
                    "close":"10",
                    "min":"10",
                    "max":"10",
                    "volume":"0.1",
                    "volumeQuote":"1"
                },
                {
                    "timestamp":"2017-05-05T16:00:00.000Z",
                    "open":"80",
                    "close":"50",
                    "min":"50",
                    "max":"80",
                    "volume":"1.679",
                    "volumeQuote":"113.95"
                }
            ],
            "ETHBTC":[
                {
                    "timestamp":"2015-08-20T19:00:00.000Z",
                    "open":"0.006",
                    "close":"0.0061",
                    "min":"0.005",
                    "max":"0.0065",
                    "volume":"0.515",
                    "volumeQuote":"0.0031271"
                },
                {
                    "timestamp":"2015-08-20T19:30:00.000Z",
                    "open":"0.0061",
                    "close":"0.00611",
                    "min":"0.00588",
                    "max":"0.0063",
                    "volume":"0.47",
                    "volumeQuote":"0.002887398"
                }
            ]
        }
        """
        params = args.DictBuilder().symbols(symbols).period(period).sort(sort).since(since).till(till).limit(limit).offset(offset).build()
        return self._public_get(endpoint='public/candles/', params=params)
    

    def get_candles_of_symbol(self, 
    symbol: str,
    period: str = None,
    sort: str = None,
    since: str = None,
    till: str = None, 
    limit: int = None,
    offset: int = None) -> Dict[str, List[Dict[str, List[Dict[str, Any]]]]]:
        """Get candles for a specified symbol.

        Candels are used for OHLC representation.

        https://api.exchange.cryptomkt.com/#candles

        :param symbol: The symbol id.
        :param period: Optional. A valid tick interval. 'M1' (one minute), 'M3', 'M5', 'M15', 'M30', 'H1' (one hour), 'H4', 'D1' (one day), 'D7', '1M' (one month). Default is 'M30'.
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'.
        :param since: Optional. Initial value of the queried interval.
        :param till: Optional. Last value of the queried interval.
        :param limit: Optional. Candles per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 

        :returns: The candles for each queried symbol.

        .. code-block:: python
        [
            {
                "timestamp":"2017-05-05T15:00:00.000Z",
                "open":"10",
                "close":"10",
                "min":"10",
                "max":"10",
                "volume":"0.1",
                "volumeQuote":"1"
            },
            {
                "timestamp":"2017-05-05T16:00:00.000Z",
                "open":"80",
                "close":"50",
                "min":"50",
                "max":"80",
                "volume":"1.679",
                "volumeQuote":"113.95"
            }
        ]
        """
        params = args.DictBuilder().period(period).sort(sort).since(since).till(till).limit(limit).offset(offset).build()
        return self._public_get(endpoint=f"public/candles/{symbol}", params=params)


    #################
    # AUTHENTICATED #
    #################

    ###########
    # TRADING #
    ###########

    def get_trading_balance(self) -> List[Dict[str, Any]]:
        """Get the trading balance.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#trading-balance

        :returns: the trading balance.

        .. code-block:: python
        [
            {
                "currency": "ETH",
                "available": "10.000000000",
                "reserved": "0.560000000"
            },
            {
                "currency": "BTC",
                "available": "0.010205869",
                "reserved": "0"
            }
        ]
        """
        return self._get(endpoint='trading/balance')

    def get_active_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Get the account active orders.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#get-active-orders

        :param symbol: Optional. A symbol for filtering active orders.

        :returns: The account active orders.

        .. code-block:: python
        [
            {
                "id": 840450210,
                "clientOrderId": "c1837634ef81472a9cd13c81e7b91401",
                "symbol": "ETHBTC",
                "side": "buy",
                "status": "partiallyFilled",
                "type": "limit",
                "timeInForce": "GTC",
                "quantity": "0.020",
                "price": "0.046001",
                "cumQuantity": "0.005",
                "postOnly": false,
                "createdAt": "2017-05-12T17:17:57.437Z",
                "updatedAt": "2017-05-12T17:18:08.610Z"
            }
        ]
        """
        params = args.DictBuilder().symbol(symbol).build()
        return self._get(endpoint='order', params=params)
    
    def get_active_order(self, client_order_id: str, wait: int= None) -> Dict[str, Any]:
        """Get an order by its client order id.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#get-active-order-by-clientorderid

        :param client_order_id: The clientOrderId of the order.
        :param wait: Optional. Time in milliseconds. Max value is 60000. Default is None. While using long polling request: if order is filled, cancelled or expired, order info will be returned instantly. For other order statuses, actual order info will be returned after specified wait time.

        :returns: An order of the account.

        .. code-block:: python
        {
            "id": 840450210,
            "clientOrderId": "c1837634ef81472a9cd13c81e7b91401",
            "symbol": "ETHBTC",
            "side": "buy",
            "status": "partiallyFilled",
            "type": "limit",
            "timeInForce": "GTC",
            "quantity": "0.020",
            "price": "0.046001",
            "cumQuantity": "0.005",
            "postOnly": false,
            "createdAt": "2017-05-12T17:17:57.437Z",
            "updatedAt": "2017-05-12T17:18:08.610Z"
        }
        """
        params = args.DictBuilder().wait(wait).build()
        return self._get(endpoint=f'order/{client_order_id}')

    def create_order(self, 
    symbol: str, 
    side: str, 
    quantity: str,
    client_order_id: str = None, 
    order_type: str = None,
    price: str = None,
    stop_price: str = None,
    time_in_force: str = None,
    expire_time: str = None,
    strict_validate: bool = None,
    post_only: bool = None) -> Dict[str, Any]:
        """Creates a new order.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#create-new-order

        :param symbol: Trading symbol.
        :param side: 'buy' or 'sell'.
        :param quantity: Order quantity.
        :param client_order_id: Optional. If given must be unique within the trading day, including all active orders. If not given, is generated by the server.
        :param order_type: Optional. 'limit', 'market', 'stopLimit' or 'stopMarket'. Default is 'limit'.
        :param time_in_force: Optional. 'GTC', 'IOC', 'FOK', 'Day', 'GTD'. Default to 'GTC'.
        :param price: Required for 'limit' and 'stopLimit'. limit price of the order.
        :param stop_price: Required for 'stopLimit' and 'stopMarket' orders. stop price of the order.
        :param expire_time: Required for orders with timeInForce = 'GDT'.
        :param strict_validate: Optional. If False, the server rounds half down for tickerSize and quantityIncrement. Example of ETHBTC: tickSize = '0.000001', then price '0.046016' is valid, '0.0460165' is invalid. 
        :param post_only: Optional. If True, your post_only order causes a match with a pre-existing order as a taker, then the order will be cancelled.

        :returns: An order of the account.

        .. code-block:: python
        {
            "id": 0,
            "clientOrderId": "d8574207d9e3b16a4a5511753eeef175",
            "symbol": "ETHBTC",
            "side": "sell",
            "status": "new",
            "type": "limit",
            "timeInForce": "GTC",
            "quantity": "0.063",
            "price": "0.046016",
            "cumQuantity": "0.000",
            "postOnly": false,
            "createdAt": "2017-05-15T17:01:05.092Z",
            "updatedAt": "2017-05-15T17:01:05.092Z"
        }
        """
        builder = args.DictBuilder().symbol(symbol).side(side).quantity(quantity).order_type(order_type).price(price).stop_price(stop_price)
        params = builder.time_in_force(time_in_force).expire_time(expire_time).strict_validate(strict_validate).post_only(post_only).build()

        if client_order_id is not None:
            return self._put(f'order/{client_order_id}', params)
        # else
        return self._post(endpoint='order', params=params)

    def cancel_all_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Cancel all active orders, or all active orders for a specified symbol.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#cancel-orders

        :param symbol: Optional. If given, cancels all orders of the symbol. If not given, cancels all orders of all symbols.

        :returns: A list with all the canceled orders.
        """
        params = args.DictBuilder().symbol(symbol).build()
        return self._delete(endpoint='order', params=params)

    def cancel_order(self, client_order_id: str) -> Dict[str, Any]:
        """Cancel the order with client_order_id.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#cancel-order-by-clientorderid

        :param client_order_id: the client id of the order to cancel.

        :returns: The canceled order.

        .. code-block:: python
        {
            "id": 0,
            "clientOrderId": "d8574207d9e3b16a4a5511753eeef175",
            "symbol": "ETHBTC",
            "side": "sell",
            "status": "canceled",
            "type": "limit",
            "timeInForce": "GTC",
            "quantity": "0.063",
            "price": "0.046016",
            "cumQuantity": "0.000",
            "postOnly": false,
            "createdAt": "2017-05-15T17:01:05.092Z",
            "updatedAt": "2017-05-15T17:01:05.092Z"
        }
        """
        return self._delete(endpoint=f'order/{client_order_id}')

    def get_trading_commission(self, symbol: str):
        """Get personal trading commission rates for a symbol.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#get-trading-commission

        :param symbol: The symbol of the comission rates.

        :returns: The commission rate for a symbol.
        """
        return self._get(endpoint=f'trading/fee/{symbol}')

    ###################
    # TRADING HISTORY #
    ###################

    def get_orders_by_client_order_id(self, client_order_id: str) -> Dict[str, Any]:
        """Get order of the account with client_order_id.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#orders-history

        :param client_order_id: the clientOrderId of the orders.

        :returns: An order list.

        .. code-block:: python
        [
            {
                "id": 828680667,
                "clientOrderId": "f4307c6e507e49019907c917b6d7a084",
                "symbol": "ETHBTC",
                "side": "sell",
                "status": "partiallyFilled",
                "type": "limit",
                "timeInForce": "GTC",
                "quantity": "13.942",
                "price": "0.011384",
                "avgPrice": "0.045000",
                "cumQuantity": "5.240",
                "createdAt": "2017-01-16T14:18:50.321Z",
                "updatedAt": "2017-01-19T15:23:56.876Z"
            }
        ]
        """
        params = args.DictBuilder().client_order_id(client_order_id).build()
        return self._get(endpoint='history/order', params=params)
        
    
    def get_orders_history(self, 
    symbol: str = None,
    since: str = None,
    till: str = None,
    limit: int = None,
    offset: int = None) -> List[Dict[str, Any]]:
        """Get the account order history.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#orders-history

        :param symbol: Optional. Filter orders by symbol.
        :param since: Optional. Initial value of the queried interval. 
        :param till: Optional. Last value of the queried interval.
        :param limit: Optional. Orders per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 

        :returns: Orders in the interval.

        .. code-block:: python
        [
            {
                "id": 828680665,
                "clientOrderId": "f4307c6e507e49019907c917b6d7a084",
                "symbol": "ETHBTC",
                "side": "sell",
                "status": "partiallyFilled",
                "type": "limit",
                "timeInForce": "GTC",
                "quantity": "13.942",
                "price": "0.011384",
                "avgPrice": "0.055487",
                "cumQuantity": "5.240",
                "createdAt": "2017-01-16T14:18:47.321Z",
                "updatedAt": "2017-01-19T15:23:54.876Z"
            },
            {
                "id": 828680667,
                "clientOrderId": "f4307c6e507e49019907c917b6d7a084",
                "symbol": "ETHBTC",
                "side": "sell",
                "status": "partiallyFilled",
                "type": "limit",
                "timeInForce": "GTC",
                "quantity": "13.942",
                "price": "0.011384",
                "avgPrice": "0.045000",
                "cumQuantity": "5.240",
                "createdAt": "2017-01-16T14:18:50.321Z",
                "updatedAt": "2017-01-19T15:23:56.876Z"
            }
        ]
        """
        params = args.DictBuilder().symbol(symbol).since(since).till(till).limit(limit).offset(offset).build()
        return self._get(endpoint='history/order', params=params)

    def get_trades_history(self,
    symbol: str = None,
    sort: str = None,
    by: str = None,
    since: str = None,
    till: str = None,
    limit: int = None,
    offset: int = None,
    margin: str = None) -> List[Dict[str, Any]]:
        """Get the account's trading history.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#trades-history

        :param symbol: Optional. Filter trades by symbol.
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'.
        :param by: Optional. Defines the sorting type.'timestamp' or 'id'. Default is 'timestamp'.
        :param since: Optional. Initial value of the queried interval. As id or as Datetime.
        :param till: Optional. Last value of the queried interval. As id or as Datetime.
        :param limit: Optional. Trades per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 
        :param margin: Optional. Filtering of margin orders. 'include', 'only' or 'ignore'. Default is 'include'

        :returns: Trades in the interval.

        .. code-block:: python
        [
            {
                "id": 9535486,
                "orderId": 816088377,
                "clientOrderId": "f8dbaab336d44d5ba3ff578098a68454",
                "symbol": "ETHBTC",
                "side": "sell",
                "quantity": "0.061",
                "price": "0.045487",
                "fee": "0.000002775",
                "timestamp": "2017-05-17T12:32:57.848Z"
            },
            {
                "id": 9535437,
                "orderId": 816088021,
                "clientOrderId": "27b9bfc068b44194b1f453c7af511ed6",
                "symbol": "ETHBTC",
                "side": "buy",
                "quantity": "0.038",
                "price": "0.046000",
                "fee": "-0.000000174",
                "timestamp": "2017-05-17T12:30:57.848Z"
            }
        ]
        """
        params = args.DictBuilder().symbol(symbol).sort(sort).by(by).since(since).till(till).limit(limit).offset(offset).margin(margin).build()
        return self._get(endpoint='history/trades', params=params)

    # TODO this method does not get trades, the problem is in the docs
    def get_trades_by_order(self, order_id: str) -> List[Dict[str, Any]]:
        """Get the account's trading order with a specified order id.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#trades-by-order

        :param order_id: Order unique identifier assigned by exchange.
  
        :returns: The trades of an order.

        TODO: example does not look like a trade, instead looks like an order
        .. code-block:: python
        [           
            {
                "id": 828680665,
                "orderId": 816088021,
                "clientOrderId": "f4307c6e507e49019907c917b6d7a084",
                "symbol": "ETHBTC",
                "side": "sell",
                "status": "partiallyFilled",
                "type": "limit",
                "timeInForce": "GTC",
                "price": "0.011384",
                "quantity": "13.942",
                "postOnly": false,
                "cumQuantity": "5.240",
                "createdAt": "2017-01-16T14:18:47.321Z",
                "updatedAt": "2017-01-19T15:23:54.876Z"
            }
        ]
        """
        return self._get(endpoint=f'history/order/{order_id}/trades')

    ######################
    # ACCOUNT MANAGEMENT #
    ######################

    def get_account_balance(self) -> List[Dict[str, Any]]:
        """Get the account balance.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#account-balance

        :returns: The account balance.

        .. code-block:: python
        [
            {
                "currency": "BTC",
                "available": "0.0504600",
                "reserved": "0.0000000"
            },
            {
                "currency": "ETH",
                "available": "30.8504600",
                "reserved": "0.0000000"
            }
        ]
        """
        return self._get(endpoint='account/balance')

    def get_deposit_crypto_address(self, currency: str) -> Dict[str, Any]:
        """Get the current address of a currency.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#deposit-crypto-address

        :param currency: currency to get the address.

        :returns: The current address for the currency.

        .. code-block:: python
        {
            "address": "NXT-G22U-BYF7-H8D9-3J27W",
            "publicKey": "f79779a3a0c7acc75a62afe8125de53106c6a19c1ebdf92a3598676e58773df0"
        }
        """
        return self._get(endpoint=f'account/crypto/address/{currency}')

    def create_deposit_crypto_address(self, currency:str) -> Dict[str, Any]:
        """Creates a new address for the currency.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#deposit-crypto-address

        :param currency: currency to create a new address.

        :returns: The created address.

        .. code-block:: python
        {
            "address": "NXT-G22U-BYF7-H8D9-3J27W",
            "publicKey": "f79779a3a0c7acc75a62afe8125de53106c6a19c1ebdf92a3598676e58773df0"
        }
        """
        return self._post(endpoint=f'account/crypto/address/{currency}')

    
    def last_10_deposit_crypto_address(self, currency: str) -> List[Dict[str, Any]]:
        """Get the last 10 addresses used for deposit by currency.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#last-10-deposit-crypto-address

        :param currency: currency to get the list of addresses.

        :returns: A list of addresses.

        .. code-block:: python
        [
            {
                "address": "NXT-G22U-BYF7-H8D9-3J27W",
                "publicKey": "f79779a3a0c7acc75a62afe8125de53106c6a19c1ebdf92a3598676e58773df0"
            }
        ]
        """
        return self._get(endpoint=f'account/crypto/addresses/{currency}')

    def last_10_used_crypto_address(self, currency: str) -> List[Dict[str, Any]]:
        """Get the last 10 unique addresses used for withdraw by currency.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#last-10-used-crypto-address

        :param currency: currency to get the list of addresses.

        :returns: A list of addresses.

        .. code-block:: python
        [
            {
                "address": "NXT-G22U-BYF7-H8D9-3J27W",
                "paymentId": "f79779a3a0c7acc75a62afe8125de53106c6a19c1ebdf92a3598676e58773df0"
            }
        ]
        """
        return self._get(endpoint=f'account/crypto/used-addresses/{currency}')
    
    def withdraw_crypto(self,
    currency: str,
    amount: str,
    address: str,
    payment_id: str = None,
    include_fee: bool = None,
    auto_commit: bool = None) -> str:
        """Withdraw cryptocurrency.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#withdraw-crypto

        :param currency: currency code of the crypto to withdraw.
        :param amount: the amount to be sent to the specified address.
        :param address: the address identifier.
        :param paymentId: Optional.
        :param includeFee: Optional. If True then the total spent amount includes fees. Default False.
        :param autoCommit: Optional. If False then you should commit or rollback transaction in an hour. Used in two phase commit schema. Default True.

        :returns: The transaction id, asigned by the exchange.

        .. code-block:: python
        "d2ce578f-647d-4fa0-b1aa-4a27e5ee597b"
        """
        params = args.DictBuilder().currency(currency).address(address).amount(amount).payment_id(payment_id).include_fee(include_fee).auto_commit(auto_commit).build()
        return self._post(endpoint='account/crypto/withdraw', params=params)['id']

    def transfer_convert_between_currencies(self, 
    from_currency: str, 
    to_currency: str, 
    amount: str) -> List[str]:
        """Converts between currencies.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#transfer-convert-between-currencies

        :param from_currency: currency code of origin.
        :param to_currency: currency code of destiny.
        :param amount: the amount to be sent. 

        :returns: A list of transaction identifiers.

        .. code-block:: python
        ["d2ce578f-647d-4fa0-b1aa-4a27e5ee597b", "d2ce57hf-6g7d-4ka0-b8aa-4a27e5ee5i7b"]
        """
        params = args.DictBuilder().from_currency(from_currency).to_currency(to_currency).amount(amount).build()
        return self._post(endpoint='account/crypto/transfer-convert', params=params)['result']
    

    def commit_withdraw_crypto(self, id: str) -> bool:
        """Commit a withdrawal of cryptocurrency.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#withdraw-crypto-commit-or-rollback

        :param id: the withdrawal transaction identifier.
        
        :returns: The transaction result. True if the commit is successful.

        .. code-block:: python
        True
        """
        return self._put(endpoint=f'account/crypto/withdraw/{id}')['result']

    def rollback_withdraw_crypto(self, id: str) -> bool:
        """Rollback a withdrawal of cryptocurrency.

        Requires authetication.

        https://api.exchange.cryptomkt.com/#withdraw-crypto-commit-or-rollback

        :param id: the withdrawal transaction identifier.
        
        :returns: The transaction result. True if the rollback is successfull.

        .. code-block:: python
        True
        """
        return self._delete(endpoint=f'account/crypto/withdraw/{id}')['result']
    
    def get_estimate_withdraw_fee(self, currency: str, amount: str) -> str:
        """Get an estimate of the withdrawal fee.

        Requires authetication.

        https://api.exchange.cryptomkt.com/#estimate-withdraw-fee

        :param currency: Currency code for withdraw.
        :param amount: Expected withdraw amount.
        
        :returns: The expected fee

        .. code-block:: python
        "0.0008"
        """
        params = args.DictBuilder().currency(currency).amount(amount).build()
        return self._get(endpoint='account/crypto/estimate-withdraw', params=params)['fee']


    def check_if_crypto_address_is_mine(self, address: str):
        """Check if an address is from this account.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#check-if-crypto-address-belongs-to-current-account

        :param address: The address to check.
        
        :returns: The transaction result. True if it is from the current account.

        .. code-block:: python
        True
        """
        return self._get(endpoint=f'account/crypto/is-mine/{address}')['result']

    def transfer_money_from_trading_balance_to_bank_balance(self,
    currency: str,
    amount: str) -> str:
        """Transfer money from trading account and a bank account.
        
        Requires authentication.

        https://api.exchange.cryptomkt.com/#transfer-money-between-trading-account-and-bank-account

        :param currency: Currency code for transfering.
        :param amount: Amount to be transfered between balances.
        
        :returns: The transaction identifier of the transfer.

        .. code-block:: python
        "d2ce578f-647d-4fa0-b1aa-4a27e5ee597b"
        """
        params = args.DictBuilder().currency(currency).amount(amount).transfer_type(args.TRANSFER_TYPE.EXCHANGE_TO_BANK).build()
        return self._post(endpoint='account/transfer', params=params)['id']

    def transfer_money_from_bank_balance_to_trading_balance(self, 
    currency: str, 
    amount: str) -> str:
        """Transfer money from bank account to trading account.
        
        Requires authentication.

        https://api.exchange.cryptomkt.com/#transfer-money-between-trading-account-and-bank-account

        :param currency: Currency code for transfering.
        :param amount: Amount to be transfered between balances.
        
        :returns: The transaction identifier of the transfer.

        .. code-block:: python
        "d2ce578f-647d-4fa0-b1aa-4a27e5ee597b"
        """
        params = args.DictBuilder().currency(currency).amount(amount).transfer_type(args.TRANSFER_TYPE.BANK_TO_EXCHANGE).build()
        return self._post(endpoint='account/transfer', params=params)['id']

    def transfer_money_to_another_user(self, 
    currency: str, 
    amount: str, 
    transfer_by: str, 
    identifier: str) -> Dict[str, str]:
        """Transfer money to another user.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#transfer-money-to-another-user-by-email-or-username

        :param currency: currency code.
        :param amount: amount to be transfered between balances.
        :param by: either 'email' or 'username'.
        :param identifier: the email or the username.
        
        :returns: The transaction identifier of the transfer.

        .. code-block:: python
        "fd3088da-31a6-428a-b9b6-c482673ff0f2"
        """
        params = args.DictBuilder().currency(currency).amount(amount).transfer_by(transfer_by).identifier(identifier).build()
        return self._post(endpoint='account/transfer/internal', params=params)['result']

    def get_transactions_history(self,
    currency: str,
    sort: str = None,
    by: str = None,
    since: str = None,
    till: str = None,
    limit: int = None,
    offset: int = None,
    show_senders: bool = None) -> List[Dict[str, Any]]:
        """Get the transactions of the account by currency.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#get-transactions-history

        :param currency: Currency code to get the transaction history.
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'.
        :param by: Optional. Defines the sorting type.'timestamp' or 'id'. Default is 'timestamp'.
        :param since: Optional. Initial value of the queried interval. As id or as Datetime.
        :param till: Optional. Last value of the queried interval. As id or as Datetime.
        :param limit: Optional. Transactions per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 
        :param show_senders: Optional. If True, show the sender address for payins.

        :returns: A list with the transactions in the interval.

        .. code-block:: python
        [
            {
                "id": "6a2fb54d-7466-490c-b3a6-95d8c882f7f7",
                "index": 20400458,
                "currency": "ETH",
                "amount": "38.616700000000000000000000",
                "fee": "0.000880000000000000000000",
                "address": "0xfaEF4bE10dDF50B68c220c9ab19381e20B8EEB2B",        
                "hash": "eece4c17994798939cea9f6a72ee12faa55a7ce44860cfb95c7ed71c89522fe8",
                "status": "pending",
                "type": "payout",
                "createdAt": "2017-05-18T18:05:36.957Z",
                "updatedAt": "2017-05-18T19:21:05.370Z"
            }
        ]
        """
        params = args.DictBuilder().currency(currency).sort(sort).by(by).since(since).till(till).limit(limit).offset(offset).show_senders(show_senders).build()
        return self._get(endpoint='account/transactions', params=params)
    
    def get_transaction(self, id: str) -> Dict[str, Any]:
        """Get the transactions of the account by its identifier.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#get-transactions-history

        :param id: The identifier of the transaction.

        :returns: The transaction with the given id.

        .. code-block:: python
        {
            "id": "6a2fb54d-7466-490c-b3a6-95d8c882f7f7",
            "index": 20400458,
            "currency": "ETH",
            "amount": "38.616700000000000000000000",
            "fee": "0.000880000000000000000000",
            "address": "0xfaEF4bE10dDF50B68c220c9ab19381e20B8EEB2B",        
            "hash": "eece4c17994798939cea9f6a72ee12faa55a7ce44860cfb95c7ed71c89522fe8",
            "status": "pending",
            "type": "payout",
            "createdAt": "2017-05-18T18:05:36.957Z",
            "updatedAt": "2017-05-18T19:21:05.370Z"
        }
        """
        return self._get(endpoint=f'account/transactions/{id}')
