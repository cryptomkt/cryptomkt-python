from typing import Any, Dict, List, Union

import cryptomarket.args as args
from cryptomarket.websockets.client_auth import ClientAuth

class AccountClient(ClientAuth):
    """AccountClient connects via websocket to cryptomarket to get account information of the user. uses SHA256 as auth method and authenticates automatically.

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
        super(AccountClient, self).__init__(
            "wss://api.exchange.cryptomkt.com/api/2/ws/account", 
            api_key, 
            api_secret, 
            subscription_keys={
                # transaction
                "subscribeTransactions":"transaction",
                "unsubscribeTransactions":"transaction",
                "updateTransaction":"transaction",
                # balance
                "unsubscribeBalance":"balance", 
                "subscribeBalance":"balance",
                "balance":"balance",
            },
            on_connect=on_connect, 
            on_error=on_error, 
            on_close=on_close
        )

    def get_account_balance(self, callback: callable):
        """Get the user account balance.

        https://api.exchange.cryptomkt.com/#request-balance

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
        self.send_by_id(method='getBalance', callback=callback)

    def find_transactions(
        self,
        callback: callable,
        currency: str = None,
        sort: str = None,
        since: str = None,
        till: str = None,
        limit: int = None,
        offset: int = None,
        show_senders: bool = None
    ):
        """Get a list of transactions of the account. Accepts only filtering by Datetime
        
        https://api.exchange.cryptomkt.com/#find-transactions

        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).
        :param currency: Currency code to get the transaction history.
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'.
        :param since: Optional. Initial value of the queried interval. As Datetime.
        :param till: Optional. Last value of the queried interval. As Datetime.
        :param limit: Optional. Transactions per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 
        :param show_senders: Optional. If True, show the sender address for payins.

        :returns: A list with the transactions in the interval.

        .. code-block:: python
        [
            {
                "id": "d91b8caa-ebaa-4254-b50c-8ac717016734",
                "index": 7173628127,
                "type": "exchangeToBank",
                "status": "success",
                "currency": "BTG",
                "amount": "0.00001000",
                "createdAt": "2021-01-31T08:19:48.140Z",
                "updatedAt": "2021-01-31T08:19:48.211Z"
            }
        ]
        """
        params = args.DictBuilder().currency(currency).sort(sort).since(since).till(till).limit(limit).offset(offset).show_senders(show_senders).build()
        self.send_by_id("findTransactions", callback, params)

    def load_transactions(
        self,
        callback: callable,
        currency: str = None,
        sort: str = None,
        since: str = None,
        till: str = None,
        limit: int = None,
        offset: int = None,
        show_senders: bool = None
    ):
        """Get a list of transactions of the account. Accepts only filtering by Index.

        https://api.exchange.cryptomkt.com/#load-transactions

        :param callback: A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).
        :param currency: Currency code to get the transaction history.
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'ASC'.
        :param since: Optional. Initial value of the queried interval. As id.
        :param till: Optional. Last value of the queried interval. As id.
        :param limit: Optional. Transactions per query. Defaul is 100. Max is 1000.
        :param offset: Optional. Default is 0. Max is 100000. 
        :param show_senders: Optional. If True, show the sender address for payins.

        :returns: A list with the transactions in the interval.

        .. code-block:: python
        [
            {
            "id": "76b70d1c-3dd7-423e-976e-902e516aae0e",
            "index": 7173627250,
            "type": "bankToExchange",
            "status": "success",
            "currency": "BTG",
            "amount": "0.00001000",
            "createdAt": "2021-01-31T08:19:33.892Z",
            "updatedAt": "2021-01-31T08:19:33.967Z"
            }
        ]
        """
        params = args.DictBuilder().currency(currency).sort(sort).since(since).till(till).limit(limit).offset(offset).show_senders(show_senders).build()
        self.send_by_id("loadTransactions", callback, params)

    #################
    # subscriptions #
    #################
    

    def subscribe_to_transactions(self, callback: callable, result_callback: callable=None):
        """Subscribe to a feed of transactions of the account.

        A transaction notification occurs each time the transaction has been changed:
        such as creating a transaction, updating the pending state (for example the hash assigned)
        or completing a transaction. This is the easiest way to track deposits or develop real-time asset monitoring.

        A combination of the recovery mechanism and transaction subscription provides reliable and consistent information
        regarding transactions. For that, you should store the latest processed index and
        requested possible gap using a "loadTransactions" method after connecting or reconnecting the Websocket.

        https://api.exchange.cryptomkt.com/#subscription-to-the-transactions

        :param callback: A callable to call with each update of the result data. It takes one argument, the transaction feed.
        :param result_callback: A callable to call with the subscription result. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: A transaction of the account as feed for the callback.

        .. code-block:: python
        {
            "id": "76b70d1c-3dd7-423e-976e-902e516aae0e",
            "index": 7173627250,
            "type": "bankToExchange",
            "status": "success",
            "currency": "BTG",
            "amount": "0.00001000",
            "createdAt": "2021-01-31T08:19:33.892Z",
            "updatedAt": "2021-01-31T08:19:33.967Z"
        }
        """
        self.send_subscription(method='subscribeTransactions', callback=callback, params={}, result_callback=result_callback)
    
    def unsubscribe_to_transactions(self, callback: callable=None):
        """unsubscribe to the transaction feed.

        https://api.exchange.cryptomkt.com/#subscription-to-the-transactions

        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The operation result as result argument for the callback. True if success.
        """
        self.send_unsubscription(method='unsubscribeTransactions', callback=callback)

    def subscribe_to_balance(self, callback: callable, result_callback: callable=None):
        """Subscribe to the balance of the account.

        This subscription aims to provide an easy way to be informed of the current balance state. 
        If the state has been changed or potentially changed the "balance" event will come with the actual state. 
        Please be aware that only non-zero values are present.

        https://api.exchange.cryptomkt.com/#subscription-to-the-balance

        :param callback: A callable to call with each update of the result data. It takes one argument, the balance feed, a list of balances.
        :param result_callback: A callable to call with the subscription result. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: A list of balances of the account as feed for the callback.

        .. code-block:: python
        [
            {
                "currency": "BTC",
                "available": "0.00005821",
                "reserved": "0"
            },
            {
                "currency": "DOGE",
                "available": "11",
                "reserved": "0"
            }
        ]
        """
        self.send_subscription(method='subscribeBalance', callback=callback, params={}, result_callback=result_callback)

    def unsubscribe_to_balance(self, callback: callable=None):
        """unsubscribe to the balance feed.

        https://api.exchange.cryptomkt.com/#subscription-to-the-balance

        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The operation result as result argument for the callback. True if success.
        """
        self.send_unsubscription(method='unsubscribeBalance', callback=callback)
