from enum import Enum
from typing import Callable, List, Optional, Union

from dacite import Config, DaciteError, from_dict
from typing_extensions import Literal

import cryptomarket.args as args
from cryptomarket.dataclasses.balance import Balance
from cryptomarket.dataclasses.commission import Commission
from cryptomarket.dataclasses.report import Report
from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.websockets.client_auth import ClientAuthenticable
from cryptomarket.websockets.subscriptionMethodData import \
    SubscriptionMethodData

_REPORTS = 'reports'
_BALANCES = 'balances'


class TradingClient(ClientAuthenticable):
    """TradingClient connects via websocket to cryptomarket to enable the user to manage orders. uses SHA256 as auth method and authenticates automatically.

    :param api_key: the user api key
    :param api_secret: the user api secret
    :param window: Maximum difference between timestamp and the moment of request processing in milliseconds for api calls. Max is 60_000. Default is 10_000
    :param on_connect: function called on a successful connection. no parameters
    :param on_error: function called on a websocket error, and called in an authenticated error. it takes one parameter, the error.
    :param on_close: function called on the closing event of the websocket. no parameters
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        window: int = None,
        on_connect: Optional[Callable[[], None]] = None,
        on_error: Optional[Callable[[], None]] = None,
        on_close: Optional[Callable[[], None]] = None,
    ):
        super(TradingClient, self).__init__(
            "wss://api.exchange.cryptomkt.com/api/3/ws/trading",
            api_key=api_key,
            api_secret=api_secret,
            window=window,
            subscription_methods_data={
                # reports
                'spot_order': SubscriptionMethodData(_REPORTS, 'update'),
                'spot_orders': SubscriptionMethodData(_REPORTS, 'snapshot'),
                'spot_subscribe': SubscriptionMethodData(_REPORTS, 'command'),
                'spot_unsubscribe': SubscriptionMethodData(_REPORTS, 'command'),
                # spot balance
                'spot_balance': SubscriptionMethodData(_BALANCES, 'snapshot'),
                'spot_balance_subscribe': SubscriptionMethodData(_BALANCES, 'command'),
                'spot_balance_unsubscribe': SubscriptionMethodData(_BALANCES, 'command'),
            },
            on_connect=on_connect,
            on_error=on_error,
            on_close=on_close
        )

    def subscribe_to_reports(
        self,
        callback: Callable[[List[Report], Literal['snapshot', 'update']], None],
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[bool, None]], None]] = None,
    ):
        """subscribe to a feed of execution reports of the user's orders

        https://api.exchange.cryptomkt.com/#socket-spot-trading

        :param callback: callable that recieves a list of reports.
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the result of the subscription. True if successful
        """
        def intercept_feed(feed, feed_type):
            if isinstance(feed, list):
                callback(
                    [from_dict(data_class=Report, data=data) for data in feed],
                    feed_type)
            else:
                callback(
                    [from_dict(data_class=Report, data=feed)],
                    feed_type)
        self._send_subscription(
            'spot_subscribe',
            callback=intercept_feed,
            result_callback=result_callback
        )

    def unsubscribe_to_reports(
        self,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[bool, None]], None]] = None,
    ):
        """stop recieveing the report feed subscription

        https://api.exchange.cryptomkt.com/#socket-spot-trading

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or the result of the unsubscription. True if successful
        """
        self._send_unsubscription(
            'spot_unsubscribe',
            callback=callback
        )

    def subscribe_to_spot_balance(
        self,
        mode: Union[args.SubscriptionMode, Literal['updates', 'batches']],
        callback: Callable[[List[Balance]], None],
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[bool, None]], None]] = None,
    ):
        """subscribe to a feed of the user's spot balances

        only non-zero values are present

        https://api.exchange.cryptomkt.com/#subscribe-to-spot-balances

        :param mode: Either 'updates' or 'batches'. Update messages arrive after an update. Batch messages arrive at equal intervals after an update
        :param callback: callable that recieves a list of balances.
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the result of the subscription. True if successful
        """
        params = args.DictBuilder().subscription_mode(mode).build()

        def intercept_feed(feed, feed_type):
            if isinstance(feed, list):
                callback([from_dict(data_class=Balance, data=balance)
                          for balance in feed])
            else:
                callback([from_dict(data_class=Balance, data=feed)])

        self._send_subscription(
            'spot_balance_subscribe',
            callback=intercept_feed,
            result_callback=result_callback,
            params=params
        )

    def unsubscribe_to_spot_balance(
        self,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[bool, None]], None]] = None,
    ):
        """stop recieving the feed of balances

        https://api.exchange.cryptomkt.com/#subscribe-to-spot-balances

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or the result of the unsubscription. True if successful
        """
        params = args.DictBuilder().subscription_mode(
            args.SubscriptionMode.UPDATES).build()
        self._send_unsubscription(
            'spot_balance_unsubscribe', callback=callback, params=params)

    def get_active_spot_orders(
        self,
        callback: Callable[[
            Union[CryptomarketAPIException, None], Union[List[Report], None]], None]
    ):
        """Get the user's active spot orders

        https://api.exchange.cryptomkt.com/#get-active-spot-orders

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or the list of reports of the active spot orders
        """
        def intercept_response(err, response):
            if err:
                callback(err, None)
                return
            reports = [from_dict(data_class=Report, data=report)
                       for report in response]
            callback(None, reports)
        self._send_by_id('spot_get_orders', callback=intercept_response)

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
        client_order_id: Optional[str] = None,
        price: Optional[str] = None,
        stop_price: Optional[str] = None,
        expire_time: Optional[str] = None,
        post_only: Optional[bool] = None,
        take_rate: Optional[str] = None,
        make_rate: Optional[str] = None,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[Report, None]], None]] = None,
    ):
        """Creates a new spot order

        For fee, for price accuracy and quantity, and for order status information see the api docs at https://api.exchange.cryptomkt.com/#create-new-spot-order

        https://api.exchange.cryptomkt.com/#place-new-spot-order

        :param symbol: Trading symbol
        :param side: Either 'buy' or 'sell'
        :param quantity: Order quantity
        :param client_order_id: Optional. If given must be unique within the trading day, including all active orders. If not given, is generated by the server
        :param type: Optional. 'limit', 'market', 'stopLimit', 'stopMarket', 'takeProfitLimit' or 'takeProfitMarket'. Default is 'limit'
        :param time_in_force: Optional. 'GTC', 'IOC', 'FOK', 'Day' or 'GTD'. Default to 'GTC'
        :param price: Optional. Required for 'limit' and 'stopLimit'. limit price of the order
        :param stop_price: Optional. Required for 'stopLimit' and 'stopMarket' orders. stop price of the order
        :param expire_time: Optional. Required for orders with timeInForce = GDT
        :param strict_validate: Optional. If False, the server rounds half down for tickerSize and quantityIncrement. Example of ETHBTC: tickSize = '0.000001', then price '0.046016' is valid, '0.0460165' is invalid
        :param post_only: Optional. If True, your post_only order causes a match with a pre-existing order as a taker, then the order will be cancelled
        :param take_rate: Optional. Liquidity taker fee, a fraction of order volume, such as 0.001 (for 0.1% fee). Can only increase the fee. Used for fee markup.
        :param make_rate: Optional. Liquidity provider fee, a fraction of order volume, such as 0.001 (for 0.1% fee). Can only increase the fee. Used for fee markup.
        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a report of the created order
        """
        params = args.DictBuilder().symbol(symbol).side(side).quantity(quantity).order_type(type).time_in_force(time_in_force).client_order_id(
            client_order_id).price(price).stop_price(stop_price).expire_time(expire_time).post_only(post_only).take_rate(take_rate).make_rate(make_rate).build()

        if callback:
            def intercept_response(err, response):
                if err:
                    callback(err, None)
                    return
                callback(None, from_dict(data_class=Report,
                         data=response, config=Config(cast=[Enum])))
        else:
            intercept_response = None
        self._send_by_id(
            'spot_new_order',
            callback=intercept_response,
            params=params
        )

    def create_spot_order_list(
        self,
        contingency_type: Union[args.ContingencyType, Literal['allOrNone', 'oneCancelOther', 'oneTriggerOneCancelOther']],
        orders: List[args.OrderRequest],
        order_list_id: Optional[str] = None,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[Report, None]], None]] = None
    ):
        """creates a list of spot orders

        calls the callback once per each order in the orders list

        Types or Contingency:
        - Contingency.ALL_OR_NONE (Contingency.AON)
        - Contingency.ONE_CANCEL_OTHER (Contingency.OCO)
        - Contingency.ONE_TRIGGER_ONE_CANCEL_OTHER (Contingency.OTOCO)

        Restriction in the number of orders:
        - An AON list must have 2 or 3 orders
        - An OCO list must have 2 or 3 orders, and only one can be a limit order
        - An OTO list must have 2 or 3 orders
        - An OTOCO must have 3 or 4 orders, and for the secondary only one can be a limit order

        Symbol restrictions:
        - For an AON order list, the symbol code of orders must be unique for each order in the list.
        - For an OCO order list, there are no symbol code restrictions.
        - For an OTOCO order list, the symbol code of orders must be the same for all orders in the list (placing orders in different order books is not supported).

        OrderType restrictions:
        - For an AON order list, orders must be OrderType.LIMIT or OrderType.Market
        - For an OCO order list, orders must be OrderType.LIMIT, OrderType.STOP_LIMIT, OrderType.STOP_MARKET, OrderType.TAKE_PROFIT_LIMIT or OrderType.TAKE_PROFIT_MARKET.
        - An OCO order list cannot include more than one limit order (the same
        applies to secondary orders in an OTOCO order list).
        - For an OTOCO order list, the first order must be OrderType.LIMIT, OrderType.MARKET, OrderType.STOP_LIMIT, OrderType.STOP_MARKET, OrderType.TAKE_PROFIT_LIMIT or OrderType.TAKE_PROFIT_MARKET.
        - For an OTOCO order list, the secondary orders have the same restrictions as an OCO order
        - Default is OrderType.Limit

        TimeInForce restrictions:
        - For an AON order list, required and must be FOK
        - For an OCO order list is optional, orders can be GTC, IOC (except limit orders), FOK (except limit orders), DAY or GTD
        - For an OTOCO order list, the first order can be GTC, IOC, FOK, DAY, GTD
        - For an OTOCO order list is optional, the secondary orders can be orders must be GTC, IOC (except limit orders), FOK (except limit orders), DAY or GTD

        https://api.exchange.cryptomkt.com/#create-new-spot-order-list-2

        :param contingency_type: order list type.
        :param orders: the list of orders
        :param order_list_id: order list identifier. If not provided, it will be generated by the system. Must be equal to the client order id of the first order in the request
        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a report of one of the created order. Once per created order
        """
        params = args.DictBuilder().order_list_id(
            order_list_id).contingency_type(contingency_type).orders(orders).build()
        if callback:
            def intercept_response(err, response):
                if err:
                    callback(err, None)
                    return
                report = from_dict(data_class=Report,
                                   data=response, config=Config(cast=[Enum]))
                callback(None, report)
        else:
            intercept_response = None
        self._send_by_id('spot_new_order_list',
                         callback=intercept_response, params=params, call_count=len(orders))

    def cancel_spot_order(
        self,
        client_order_id: str,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[Report, None]], None]] = None
    ):
        """cancels a spot order

        https://api.exchange.cryptomkt.com/#cancel-spot-order-2

        :param client_order_id: the client order id of the order to cancel
        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a report of the canceled order
        """
        params = args.DictBuilder().client_order_id(client_order_id).build()

        if callback:
            def intercept_result(err, response):
                if err:
                    callback(err, None)
                    return
                callback(None, from_dict(data_class=Report,
                         data=response, config=Config(cast=[Enum])))
        else:
            intercept_result = None
        self._send_by_id('spot_cancel_order',
                         callback=intercept_result, params=params)

    def replace_spot_order(
        self,
        client_order_id: str,
        new_client_order_id: str,
        quantiy: str,
        price: str,
        strict_validate: Optional[bool] = None,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[Report, None]], None]] = None,
    ):
        """changes the parameters of an existing order, quantity or price

        https://api.exchange.cryptomkt.com/#cancel-replace-spot-order

        :param client_order_id: the client order id of the order to change
        :param new_client_order_id: the new client order id for the modified order. must be unique within the trading day
        :param quantity: new order quantity
        :param price: new order price
        :param strict_validate:  price and quantity will be checked for the incrementation with tick size and quantity step. See symbol's tick_size and quantity_increment
        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a report of the new version of the order
        """
        params = args.DictBuilder().client_order_id(client_order_id).new_client_order_id(
            new_client_order_id).quantity(quantiy).price(price).strict_validate(strict_validate).build()
        if callback:
            def intercept_result(err, response):
                if err:
                    callback(err, None)
                    return
                callback(None, from_dict(data_class=Report,
                         data=response, config=Config(cast=[Enum])))
        else:
            intercept_result = None
        self._send_by_id('spot_replace_order',
                         callback=intercept_result, params=params)

    def cancel_spot_orders(
        self,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[Report], None]], None]] = None,
    ):
        """cancel all active spot orders and returns the ones that could not be canceled

        https://api.exchange.cryptomkt.com/#cancel-spot-orders

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a list of reports of the canceled orders
        """
        if callback:
            def intercept_result(err, response):
                if err:
                    callback(err, None)
                    return
                reports = [from_dict(data_class=Report, data=report, config=Config(cast=[Enum]))
                           for report in response]
                callback(None, reports)
        else:
            intercept_result = None
        self._send_by_id('spot_cancel_orders', callback=intercept_result)

    def get_spot_trading_balances(
        self,
        callback: Callable[[
            Union[CryptomarketAPIException, None], Union[List[Report], None]], None] = None,
    ):
        """Get the user's spot trading balance for all currencies with balance

        https://api.exchange.cryptomkt.com/#get-spot-trading-balances

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a list of balances
        """
        def intercept_result(err, response):
            if err:
                callback(err, None)
                return
            balances = [from_dict(data_class=Balance, data=balance)
                        for balance in response]
            callback(None, balances)
        self._send_by_id('spot_balances', callback=intercept_result)

    def get_spot_trading_balance_of_currency(
        self,
        currency: str,
        callback: Callable[[
            Union[CryptomarketAPIException, None], Union[Balance, None]], None]
    ):
        """Get the user spot trading balance of a currency

        https://api.exchange.cryptomkt.com/#get-spot-trading-balance-2

        :param currency: The currency code to query the balance
        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or the queried balance
        """
        params = args.DictBuilder().currency(currency).build()

        def intercept_result(err, response):
            if err:
                callback(err, None)
                return
            callback(None, from_dict(data_class=Balance, data=response))
        self._send_by_id(
            'spot_balance', callback=intercept_result, params=params)

    def get_spot_commisions(
        self,
        callback: Callable[[Union[CryptomarketAPIException, None], Union[List[Commission], None]], None],
    ):
        """Get the personal trading commission rates for all symbols

        https://api.exchange.cryptomkt.com/#get-spot-fees

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a list of commissions
        """
        def intercept_result(err, response):
            if err:
                callback(err, None)
                return
            commissions = [from_dict(data_class=Commission, data=commission)
                           for commission in response]
            callback(None, commissions)
        self._send_by_id('spot_fees', callback=intercept_result)

    def get_spot_commision_of_symbol(
        self,
        symbol: str,
        callback: Callable[[Union[CryptomarketAPIException, None], Union[Commission, None]], None],
    ):
        """Get the personal trading commission rate of a symbol

        https://api.exchange.cryptomkt.com/#get-spot-fee

        :param symbol: The symbol of the commission rate
        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a the queried commission
        """
        def intercept_result(err, response):
            if err:
                callback(err, None)
                return
            result = from_dict(data_class=Commission, data=response)
            callback(None, result)
        params = args.DictBuilder().symbol(symbol).build()
        self._send_by_id('spot_fee', callback=intercept_result, params=params)
