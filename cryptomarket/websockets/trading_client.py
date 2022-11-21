from typing import Callable, List, Literal, Optional, Union

from dacite import from_dict
import cryptomarket.args as args
from cryptomarket.dataclasses.balance import Balance
from cryptomarket.dataclasses.commission import Commission
from cryptomarket.dataclasses.report import Report
from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.websockets.client_auth import ClientAuth
from cryptomarket.websockets.subscriptionMethodData import SubscriptionMethodData

_REPORTS = 'reports'


class TradingClient(ClientAuth):
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
        :param result_callback: A callable that recieves the result of the subscription. True if successful
        """
        def intercept_feed(feed, feed_type):
            if isinstance(feed, list):
                callback(
                    [from_dict(data_class=Report, data=data) for data in feed],
                    feed_type
                )
            else:
                callback([from_dict(data_class=Report, data=feed)], feed_type)
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

        :param callback: A callable that recieves the result of the unsubscription. True if successful
        """
        self._send_unsubscription(
            'spot_unsubscribe',
            callback=callback
        )

    def get_active_spot_orders(
        self,
        callback: Callable[[
            Union[CryptomarketAPIException, None], Union[List[Report], None]], None]
    ):
        """Get the user's active spot orders

        https://api.exchange.cryptomkt.com/#get-active-spot-orders

        :param callback: A callable called with a list of reports of the active spot orders
        """
        def intercept_response(err, response):
            if err is not None:
                callback(err, None)
                return
            result = []
            for report in response:
                result.append(from_dict(
                    data_class=Report,
                    data=report
                ))
            callback(None, result)
        self._send_by_id('spot_get_orders', callback=intercept_response)

    def create_spot_order(
        self,
        symbol: str,
        side: Union[args.SIDE, Literal['buy', 'sell']],
        quantity: str,
        type: Optional[Union[args.ORDER_TYPE, Literal[
            'limit', 'market', 'stopLimit', 'stopMarket', 'takeProfitLimit', 'takeProfitMarket'
        ]]] = None,
        time_in_force: Optional[Union[args.TIME_IN_FORCE, Literal[
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
        :param callback: A callable called with a report of the created order
        """
        params = args.DictBuilder().symbol(symbol).side(side).quantity(quantity).order_type(type).time_in_force(time_in_force).client_order_id(
            client_order_id).price(price).stop_price(stop_price).expire_time(expire_time).post_only(post_only).take_rate(take_rate).make_rate(make_rate).build()

        def intercept_response(err, response):
            if err is not None:
                callback(err, None)
                return
            result = from_dict(
                data_class=Report,
                data=response
            )
            callback(None, result)
        self._send_by_id(
            'spot_new_order',
            callback=intercept_response,
            params=params
        )

    def create_spot_order_list(
        self,
        contingency_type: Union[args.CONTINGENCY_TYPE, Literal['allOrNone', 'oneCancelOther', 'oneTriggerOneCancelOther']],
        orders: List[args.OrderRequest],
        order_list_id: Optional[str] = None,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[Report], None]], None]] = None
    ):
        """creates a list of spot orders

        Types or contingency:

        - CONTINGENCY.ALL_OR_NONE (CONTINGENCY.AON)
        - CONTINGENCY.ONE_CANCEL_OTHER (CONTINGENCY.OCO)
        - CONTINGENCY.ONE_TRIGGER_ONE_CANCEL_OTHER (CONTINGENCY.OTOCO)

        Restriction in the number of orders:

        - An AON list must have 2 or 3 orders
        - An OCO list must have 2 or 3 orders
        - An OTOCO must have 3 or 4 orders

        Symbol restrictions:

        - For an AON order list, the symbol code of orders must be unique for each order in the list.
        - For an OCO order list, there are no symbol code restrictions.
        - For an OTOCO order list, the symbol code of orders must be the same for all orders in the list (placing orders in different order books is not supported).

        ORDER_TYPE restrictions:
        - For an AON order list, orders must be ORDER_TYPE.LIMIT or ORDER_TYPE.Market
        - For an OCO order list, orders must be ORDER_TYPE.LIMIT, ORDER_TYPE.STOP_LIMIT, ORDER_TYPE.STOP_MARKET, ORDER_TYPE.TAKE_PROFIT_LIMIT or ORDER_TYPE.TAKE_PROFIT_MARKET.
        - An OCO order list cannot include more than one limit order (the same
        applies to secondary orders in an OTOCO order list).
        - For an OTOCO order list, the first order must be ORDER_TYPE.LIMIT, ORDER_TYPE.MARKET, ORDER_TYPE.STOP_LIMIT, ORDER_TYPE.STOP_MARKET, ORDER_TYPE.TAKE_PROFIT_LIMIT or ORDER_TYPE.TAKE_PROFIT_MARKET.
        - For an OTOCO order list, the secondary orders have the same restrictions as an OCO order
        - Default is ORDER_TYPE.Limit

        https://api.exchange.cryptomkt.com/#create-new-spot-order-list-2

        :param contingency_type: order list type.
        :param orders: the list of orders
        :param order_list_id: order list identifier. If not provided, it will be generated by the system. Must be equal to the client order id of the first order in the request
        :param callback: A callable called with a list of reports of the created orders
        """
        params = args.DictBuilder().order_list_id(
            order_list_id).contingency_type(contingency_type).orders(orders).build()

        def intercept_response(err, response):
            if err is not None:
                callback(err, None)
                return
            result = []
            for report in response:
                result.append(from_dict(
                    data_class=Report,
                    data=report
                ))
            callback(None, result)
        self._send_by_id('spot_new_order_list',
                         callback=intercept_response, params=params)

    def cancel_spot_order(
        self,
        client_order_id: str,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[Report, None]], None]] = None
    ):
        """cancels a spot order

        https://api.exchange.cryptomkt.com/#cancel-spot-order-2

        :param client_order_id: the client order id of the order to cancel
        :param callback: A callable called with a report of the canceled order
        """
        params = args.DictBuilder().client_order_id(client_order_id).build()

        def intercept_result(err, response):
            if err is not None:
                callback(err, None)
                return
            result = from_dict(
                data_class=Report,
                data=response
            )
            callback(None, result)
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
        :param callback: A callable called a report of the new version of the order
        """
        params = args.DictBuilder().client_order_id(client_order_id).new_client_order_id(
            new_client_order_id).quantity(quantiy).price(price).strict_validate(strict_validate).build()

        def intercept_result(err, response):
            if err is not None:
                callback(err, None)
                return
            result = from_dict(
                data_class=Report,
                data=response
            )
            callback(None, result)
        self._send_by_id('spot_replace_order',
                         callback=intercept_result, params=params)

    def cancel_spot_orders(
        self,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[List[Report], None]], None]] = None,
    ):
        """cancel all active spot orders and returns the ones that could not be canceled

        https://api.exchange.cryptomkt.com/#cancel-spot-orders

        :param callback: A callable called with a list of reports of the canceled orders
        """
        def intercept_result(err, response):
            if err is not None:
                callback(err, None)
                return
            result = []
            for report in response:
                result.append(from_dict(
                    data_class=Report,
                    data=report
                ))
            callback(None, result)
        self._send_by_id('spot_cancel_orders', callback=intercept_result)

    def get_spot_trading_balances(
        self,
        callback: Callable
    ):
        """Get the user's spot trading balance for all currencies with balance

        https://api.exchange.cryptomkt.com/#get-spot-trading-balances

        :param callback: A callable called with a list of balances
        """
        def intercept_result(err, response):
            if err is not None:
                callback(err, None)
                return
            result = []
            for balance in response:
                result.append(from_dict(
                    data_class=Balance,
                    data=balance
                ))
            callback(None, result)
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
        :param callback: A callable called with a the queried balance
        """
        params = args.DictBuilder().currency(currency).build()

        def intercept_result(err, response):
            if err is not None:
                callback(err, None)
                return
            result = from_dict(
                data_class=Balance,
                data=response
            )
            callback(None, result)
        self._send_by_id(
            'spot_balance', callback=intercept_result, params=params)

    def get_spot_commisions(
        self,
        callback: Callable[[Union[CryptomarketAPIException, None], Union[List[Commission], None]], None],
    ):
        """Get the personal trading commission rates for all symbols

        https://api.exchange.cryptomkt.com/#get-spot-fees

        :param callback: A callable called with a list of commissions
        """
        def intercept_result(err, response):
            if err is not None:
                callback(err, None)
                return
            result = []
            for commission in response:
                result.append(from_dict(
                    data_class=Commission,
                    data=commission
                ))
            callback(None, result)
        self._send_by_id('spot_fees', callback=intercept_result)

    def get_spot_commision_of_symbol(
        self,
        symbol: str,
        callback: Callable[[Union[CryptomarketAPIException, None], Union[Commission, None]], None],
    ):
        """Get the personal trading commission rate of a symbol

        https://api.exchange.cryptomkt.com/#get-spot-fee

        :param symbol: The symbol of the commission rate
        :param callback: A callable called with a the queried commission
        """
        def intercept_result(err, response):
            if err is not None:
                callback(err, None)
                return
            result = from_dict(
                data_class=Commission,
                data=response
            )
            callback(None, result)
        params = args.DictBuilder().symbol(symbol).build()
        self._send_by_id('spot_fee', callback=intercept_result, params=params)
