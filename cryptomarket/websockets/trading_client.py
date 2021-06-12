from typing import Any, Dict, List, Union

import cryptomarket.args as args
from cryptomarket.websockets.client_auth import ClientAuth

class TradingClient(ClientAuth):
    """TradingClient connects via websocket to cryptomarket to enable the user to manage orders. uses SHA256 as auth method and authenticates automatically.

    :param api_key: the user api key
    :param api_secret: the user api secret
    :param on_connect: function called on a successful connection. no parameters
    :param on_error: function called on a websocket error, and called in an authenticated error. it takes one parameter, the error.
    :param on_close: function called on the closing event of the websocket. no parameters
    """
    def __init__(
        self, 
        api_key:str, 
        api_secret:str, 
        on_connect:callable=None, 
        on_error:callable=None, 
        on_close:callable=None
    ):
        super(TradingClient, self).__init__(
            "wss://api.exchange.cryptomkt.com/api/2/ws/trading", 
            api_key, 
            api_secret, 
            subscription_keys={
                "subscribeReports":"reports",
                'activeOrders':'reports',
                'report':'reports',
            },
            on_connect=on_connect, 
            on_error=on_error, 
            on_close=on_close
        )

    def create_order(
        self,
        client_order_id: str, 
        symbol: str, 
        side: str, 
        quantity: float,
        order_type: str = None,
        price: float = None,
        stop_price: float = None,
        time_in_force: str = None,
        expire_time: str = None,
        strict_validate: bool = False,
        post_only: bool = False,
        callback: callable = None
    ):
        """Creates a new order

        Requires authentication.

        https://api.exchange.cryptomkt.com/#place-new-order

        :param client_order_id: If given must be unique within the trading day, including all active orders. If not given, is generated by the server.
        :param symbol: Trading symbol.
        :param side: 'buy' or 'sell'.
        :param quantity: Order quantity.
        :param order_type: Optional. 'limit', 'market', 'stopLimit' or 'stopMarket'. Default is 'limit'.
        :param price: Required for 'limit' and 'stopLimit'. limit price of the order.
        :param stop_price: Required for 'stopLimit' and 'stopMarket' orders. stop price of the order.
        :param time_in_force: Optional. 'GTC', 'IOC', 'FOK', 'Day', 'GTD'.
        :param expire_time: Required for orders with timeInForce = 'GDT'.
        :param strict_validate: Optional. If False, the server rounds half down for tickerSize and quantityIncrement. Example of ETHBTC: tickSize = '0.000001', then price '0.046016' is valid, '0.0460165' is invalid. 
        :param post_only: Optional. If True, your post_only order causes a match with a pre-existing order as a taker, then the order will be cancelled.
        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The newly created order as result argument for the callback.

        .. code-block:: python
        {
            "id":"341065302776",
            "clientOrderId":"1000000000028",
            "symbol":"EOSETH",
            "side":"sell",
            "status":"new",
            "type":"limit",
            "timeInForce":"GTC",
            "quantity":"0.01",
            "price":"1000.0000000",
            "cumQuantity":"0.00",
            "createdAt":"2020-11-23T19:45:31.988Z",
            "updatedAt":"2020-11-23T19:45:31.988Z",
            "postOnly":False,
            "reportType":"new"
        }
        """
        builder = args.DictBuilder().client_order_id(client_order_id).symbol(symbol).side(side).quantity(quantity).order_type(order_type)
        builder.price(price).stop_price(stop_price).time_in_force(time_in_force).expire_time(expire_time)
        params = builder.strict_validate(strict_validate).post_only(post_only).build()
        self.send_by_id(method='newOrder', callback=callback, params=params)

    def cancel_order(
        self, 
        client_order_id: str, 
        callback: callable= None
    ):
        """Cancel the order with client_order_id.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#cancel-order

        :param client_order_id: The client id of the order to cancel.
        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The canceled order as result argument for the callback.

        .. code-block:: python
        {
            "id":"341065334406",
            "clientOrderId":"1000000000026",
            "symbol":"EOSETH",
            "side":"sell",
            "status":"canceled",
            "type":"limit",
            "timeInForce":"GTC",
            "quantity":"0.02",
            "price":"100.0000000",
            "cumQuantity":"0.00",
            "createdAt":"2020-11-23T19:45:31.988Z",
            "updatedAt":"2020-11-23T19:45:40.003Z",
            "postOnly":False,
            "reportType":"canceled"
        }   
        """
        params = args.DictBuilder().client_order_id(client_order_id).build()
        self.send_by_id(method='cancelOrder', callback=callback, params=params)

    def replace_order(self,
    client_order_id: str,
    request_client_id: str,
    quantity: str,
    price: str,
    strict_validate: bool = None,
    callback: callable = None,):
        """Rewrites an order, canceling it or replacing it.

        The Cancel/Replace request is used to change the parameters of an existing order and to change the quantity or price attribute of an open order.
        
        Do not use this request to cancel the quantity remaining in an outstanding order. Use the cancel_order for this purpose.
        
        It is stipulated that a newly entered order cancels a prior order that has been entered, but not yet executed.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#cancel-replace-order

        :param client_order_id: The client id of the order to modify.
        :param request_client_id: The new id for the modified order.
        :param quantity: The new quantity of the order.
        :param price: The new price of the order.
        :param strict_validate: Optional. If False, the server rounds half down for tickerSize and quantityIncrement. Example of ETHBTC: tickSize = '0.000001', then price '0.046016' is valid, '0.0460165' is invalid. 
        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The modified order as result argument for the callback.

        .. code-block:: python
        {
            "id":"341065334406",
            "clientOrderId":"1000000000026",
            "symbol":"EOSETH",
            "side":"sell",
            "status":"new",
            "type":"limit",
            "timeInForce":"GTC",
            "quantity":"0.02",
            "price":"100.0000000",
            "cumQuantity":"0.00",
            "createdAt":"2020-11-23T19:45:31.988Z",
            "updatedAt":"2020-11-23T19:45:35.006Z",
            "postOnly":False,
            "reportType":"replaced",
            "originalRequestClientOrderId":"1000000000028"
        }
        """
        builder = args.DictBuilder().client_order_id(client_order_id).request_client_id(request_client_id).quantity(quantity)
        params = builder.price(price).strict_validate(strict_validate).build()
        self.send_by_id(method='cancelReplaceOrder', callback=callback, params=params)

    def get_active_orders(self, callback: callable):
        """Get the account active orders.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#get-active-orders-2

        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The list of active orders as result argument for the callback.

        .. code-block:: python
        [
            {
                "id": "4346371528",
                "clientOrderId": "9cbe79cb6f864b71a811402a48d4b5b2",
                "symbol": "ETHBTC",
                "side": "sell",
                "status": "new",
                "type": "limit",
                "timeInForce": "GTC",
                "quantity": "0.002",
                "price": "0.083837",
                "cumQuantity": "0.000",
                "postOnly": false,
                "createdAt": "2017-10-20T12:47:07.942Z",
                "updatedAt": "2017-10-20T12:50:34.488Z",
                "reportType": "replaced",
                "originalRequestClientOrderId": "9cbe79cb6f864b71a811402a48d4b5b1"
            }
        ]
        """
        self.send_by_id(method='getOrders', callback=callback)

    def get_trading_balance(self, callback: callable):
        """Get the user trading balance.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#get-trading-balance

        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The user trading balance as result argument for the callback.

        .. code-block:: python
        [
            {
                "currency": "BCN",
                "available": "100.000000000",
                "reserved": "0"
            },
            {
                "currency": "BTC",
                "available": "0.013634021",
                "reserved": "0"
            },
            {
                "currency": "ETH",
                "available": "0",
                "reserved": "0.00200000"
            }
        ]
        """
        self.send_by_id(method='getTradingBalance', callback=callback)

    #################
    # subscriptions #
    #################
    
    def subscribe_to_reports(self, callback: callable, result_callback: callable=None):
        """Subscribe to a feed of trading events of the account.

        Requires authentication.

        https://api.exchange.cryptomkt.com/#subscribe-to-reports

        :param callback: A callable to call with each update of the result data. It takes one argument, the report feed.
        :param result_callback: A callable to call with the subscription result. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The reports of trading events of the account as feed for the callback.

        .. code-block:: python
        [
            {
                "id":"341012006539",
                "clientOrderId":"c191623deccb9a7941b9f00b2a9c513c",
                "symbol":"EOSETH",
                "side":"sell",
                "status":"new",
                "type":"limit",
                "timeInForce":"GTC",
                "quantity":"0.01",
                "price":"1000.0000000",
                "cumQuantity":"0.00",
                "createdAt":"2020-11-23T18:28:54.304Z",
                "updatedAt":"2020-11-23T18:28:54.304Z",
                "postOnly":False,
                "reportType":"status"
            },
            {
                "id": "4345697765",
                "clientOrderId": "53b7cf917963464a811a4af426102c19",
                "symbol": "ETHBTC",
                "side": "sell",
                "status": "filled",
                "type": "limit",
                "timeInForce": "GTC",
                "quantity": "0.001",
                "price": "0.053868",
                "cumQuantity": "0.001",
                "postOnly": false,
                "createdAt": "2017-10-20T12:20:05.952Z",
                "updatedAt": "2017-10-20T12:20:38.708Z",
                "reportType": "trade",
                "tradeQuantity": "0.001",
                "tradePrice": "0.053868",
                "tradeId": 55051694,
                "tradeFee": "-0.000000005"
            }
        ]
        """
        self.send_subscription(method='subscribeReports', callback=callback, params={}, result_callback=result_callback)
