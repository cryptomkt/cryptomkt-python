from enum import Enum
from typing import Callable, List, Optional, Union

from dacite import Config, from_dict
from typing_extensions import Literal

import cryptomarket.args as args
from cryptomarket.dataclasses.balance import Balance
from cryptomarket.dataclasses.transaction import Transaction
from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.websockets.client_auth import ClientAuthenticable
from cryptomarket.websockets.subscriptionMethodData import \
    SubscriptionMethodData


class WalletClient(ClientAuthenticable):
    """AccountClient connects via websocket to cryptomarket to get account information of the user. uses SHA256 as auth method and authenticates automatically.

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
        super(WalletClient, self).__init__(
            "wss://api.exchange.cryptomkt.com/api/3/ws/wallet",
            api_key=api_key,
            api_secret=api_secret,
            window=window,
            subscription_methods_data={
                # transaction
                "subscribe_transactions": SubscriptionMethodData("transaction", 'command'),
                "unsubscribe_transactions": SubscriptionMethodData("transaction", 'command'),
                "transaction_update": SubscriptionMethodData("transaction", 'update'),
                # balance
                "subscribe_wallet_balances": SubscriptionMethodData("balance", 'command'),
                "unsubscribe_wallet_balances": SubscriptionMethodData("balance", 'command'),
                "wallet_balances": SubscriptionMethodData("balance", 'snapshot'),
                "wallet_balance_update": SubscriptionMethodData("balance", 'update'),
            },
            on_connect=on_connect,
            on_error=on_error,
            on_close=on_close
        )

    def subscribe_to_transactions(
        self,
        callback: Callable[[Transaction], None],
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[bool, None]], None]] = None
    ):
        """A transaction notification occurs each time a transaction has been changed, such as creating a transaction, updating the pending state (e.g., the hash assigned) or completing a transaction

        https://api.exchange.cryptomkt.com/#subscribe-to-transactions

        :param callback: callable that recieves a transaction.
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the result of the subscription. True if successful
        """
        def intercept_feed(feed, feed_type):
            callback(from_dict(data_class=Transaction,
                     data=feed, config=Config(cast=[Enum])))
        self._send_subscription(
            'subscribe_transactions', callback=intercept_feed, result_callback=result_callback)

    def unsubscribe_to_transactions(
        self,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[bool, None]], None]] = None
    ):
        """stop recieving the feed of transactions changes

        https://api.exchange.cryptomkt.com/#subscribe-to-transactions

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or the result of the unsubscription. True if successful
        """
        self._send_unsubscription(
            'unsubscribe_transactions', callback=callback)

    def subscribe_to_wallet_balance(
        self,
        callback: Callable[[List[Balance], Literal['snapshot', 'update']], None],
        result_callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[bool, None]], None]] = None,
    ):
        """subscribe to a feed of the user's wallet balances

        only non-zero values are present

        https://api.exchange.cryptomkt.com/#subscribe-to-wallet-balance

        :param callback: callable that recieves a list of balances.
        :param result_callback: A callable of two arguments, takes either a CryptomarketAPIException, or the result of the subscription. True if successful
        """
        def intercept_feed(feed, feed_type):
            if isinstance(feed, list):
                callback([from_dict(data_class=Balance, data=balance)
                          for balance in feed],
                         feed_type)
            else:
                callback([from_dict(data_class=Balance, data=feed)],
                         feed_type)

        self._send_subscription(
            'subscribe_wallet_balances',
            callback=intercept_feed,
            result_callback=result_callback
        )

    def unsubscribe_to_wallet_balance(
        self,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[bool, None]], None]] = None,
    ):
        """stop recieving the feed of balances changes

        https://api.exchange.cryptomkt.com/#subscribe-to-wallet-balance

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or the result of the unsubscription. True if successful
        """
        self._send_unsubscription(
            'subscribe_wallet_balances', callback=callback)

    def get_wallet_balances(
        self,
        callback: Callable[[
            Union[CryptomarketAPIException, None], Union[List[Balance], None]], None],
    ):
        """Get the user's wallet balances for all currencies with balance

        https://api.exchange.cryptomkt.com/#request-wallet-balance

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a list of balances
        """
        def intercept_result(err, response):
            if err:
                callback(err, None)
                return
            balances = [from_dict(data_class=Balance, data=balance)
                        for balance in response]
            callback(None, balances)
        self._send_by_id('wallet_balances', callback=intercept_result)

    def get_wallet_balance_of_currency(
        self,
        currency: str,
        callback: Optional[Callable[[
            Union[CryptomarketAPIException, None], Union[Balance, None]], None]] = None,
    ):
        """Get the user's wallet balance of a currency

        https://api.exchange.cryptomkt.com/#request-wallet-balance

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
            'wallet_balance',
            callback=intercept_result,
            params=params
        )

    def get_transactions(
        self,
        callback: Callable[[Union[CryptomarketAPIException, None], Union[List[Transaction], None]], None],
        transaction_ids: Optional[List[str]] = None,
        type: Optional[Union[args.TransactionType, Literal[
            'DEPOSIT', 'WITHDRAW', 'TRANSFER', 'SWAP'
        ]]] = None,
        subtype: Optional[Union[args.TransactionSubType, Literal[
            'UNCLASSIFIED', 'BLOCKCHAIN', 'AIRDROP', 'AFFILIATE', 'STAKING', 'BUY_CRYPTO', 'OFFCHAIN', 'FIAT', 'SUB_ACCOUNT', 'WALLET_TO_SPOT', 'SPOT_TO_WALLET', 'WALLET_TO_DERIVATIVES', 'DERIVATIVES_TO_WALLET', 'CHAIN_SWITCH_FROM', 'CHAIN_SWITCH_TO', 'INSTANT_EXCHANGE'
        ]]] = None,
        statuses: List[Union[args.TransactionStatus, Literal[
            'CREATED', 'PENDING', 'FAILED', 'SUCCESS', 'ROLLED_BACK'
        ]]] = None,
        currencies: Optional[List[str]] = None,
        sort_by: Optional[Union[args.SortBy,
                                Literal['created_at', 'id']]] = None,
        sort: Optional[Literal['ASC', 'DESC']] = None,
        id_from: Optional[int] = None,
        id_till: Optional[int] = None,
        since: Optional[str] = None,
        till: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """Get the transaction history of the account

        Important:

        - The list of supported transaction types may be expanded in future versions

        - Some transaction subtypes are reserved for future use and do not purport to provide any functionality on the platform

        - The list of supported transaction subtypes may be expanded in future versions

        https://api.exchange.cryptomkt.com/#get-transactions

        :param callback: A callable of two arguments, takes either a CryptomarketAPIException, or a list of transactions
        :param transaction_ids: Optional. List of transaction identifiers to query
        :param type: Optional. valid types are: 'DEPOSIT', 'WITHDRAW', 'TRANSFER' and 'SWAP'
        :param subtype: Optional. valid subtypes are: 'UNCLASSIFIED', 'BLOCKCHAIN', 'AIRDROP', 'AFFILIATE', 'STAKING', 'BUY_CRYPTO', 'OFFCHAIN', 'FIAT', 'SUB_ACCOUNT', 'WALLET_TO_SPOT', 'SPOT_TO_WALLET', 'WALLET_TO_DERIVATIVES', 'DERIVATIVES_TO_WALLET', 'CHAIN_SWITCH_FROM', 'CHAIN_SWITCH_TO' and 'INSTANT_EXCHANGE'
        :param statuses: Optional. List of statuses to query. valid subtypes are: 'CREATED', 'PENDING', 'FAILED', 'SUCCESS' and 'ROLLED_BACK'
        :param currencies: Optional. List of currencies to query. If not provided it queries all currencies
        :param sort_by: Optional. sorting parameter.'created_at' or 'id'. Default is 'created_at'
        :param sort: Optional. Sort direction. 'ASC' or 'DESC'. Default is 'DESC'
        :param id_from: Optional. Interval initial value when ordering by id. Min is 0
        :param id_till: Optional. Interval end value when ordering by id. Min is 0
        :param since: Optional. Interval initial value when ordering by 'created_at'. As Datetime
        :param till: Optional. Interval end value when ordering by 'created_at'. As Datetime
        :param limit: Optional. Transactions per query. Defaul is 100. Max is 1000
        :param offset: Optional. Default is 0. Max is 100000
        """
        params = args.DictBuilder().transaction_type(type).transaction_subtype(subtype).transaction_statuses(statuses).currencies(currencies).id_from(
            id_from).id_till(id_till).tx_ids(transaction_ids).sort_by(sort_by).sort(sort).since(since).till(till).limit(limit).offset(offset).build()

        def intercept_response(err, response):
            if err is not None:
                callback(err, None)
                return
            transactions = [from_dict(data_class=Transaction, data=transaction, config=Config(cast=[Enum]))
                            for transaction in response]
            callback(None, transactions)
        self._send_by_id(
            'get_transactions',
            callback=intercept_response,
            params=params
        )
