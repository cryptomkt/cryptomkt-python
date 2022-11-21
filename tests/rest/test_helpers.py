from dataclasses import asdict
from typing import Any, Callable, Dict, List
from cryptomarket.dataclasses import (Address, Balance, Candle, Commission,
                                      Currency, MetaTransaction,
                                      NativeTransaction, Network, Order,
                                      OrderBook, OrderBookLevel, Price,
                                      PriceHistory, PricePoint, PublicTrade,
                                      Symbol, Ticker, Transaction)


# defined checks if a key is present in a dict, and if its value is str, checks if its defined.
# return false when the key is not present or when the value is an empty string, return true otherwise.
def defined(a_dict, key):
    if key not in a_dict:
        return False
    val = a_dict[key]
    if isinstance(val, str) and val == "":
        return False
    return True

# good_dict checks all of the values in the fields list to be present in the dict, and if they are
# present, check the defined() condition to be true. if any of the fields fails to be defined(), then
# this function returns false


def good_dict(a_dict: Dict[str, Any], fields: List[str]) -> bool:
    if not isinstance(a_dict, dict):
        return False
    for field in fields:
        if not defined(a_dict, field):
            return False
    return True


def good_list(check_fn: Callable[[Any], bool], list: List[Any]) -> bool:
    for elem in list:
        if not check_fn(elem):
            print(elem)
            return False
    return True


def good_currency(currency: Currency) -> bool:
    good = good_dict(
        asdict(currency),
        [
            "full_name",
            "payin_enabled",
            "payout_enabled",
            "transfer_enabled",
            "precision_transfer",
            "networks",
        ]
    )
    if not good:
        return False
    for network in currency.networks:
        if not good_network(network):
            print("***bad net***")
            return False
    return True


def good_network(network: Network):
    return good_dict(
        asdict(network),
        [
            "network",
            # "protocol",
            "default",
            "payin_enabled",
            "payout_enabled",
            "precision_payout",
            "payout_fee",
            "payout_is_payment_id",
            "payin_payment_id",
            "payin_confirmations",
            # "address_regrex",
            # "payment_id_regex",
            # "low_processing_time",
            # "high_processing_time",
            # "avg_processing_time"
        ]
    )


def good_symbol(symbol: Symbol) -> bool:
    return good_dict(
        asdict(symbol),
        [
            "type",
            "base_currency",
            "quote_currency",
            "status",
            "quantity_increment",
            "tick_size",
            "take_rate",
            "make_rate",
            "fee_currency",
            # "margin_trading",
            # "max_initial_leverage",
        ]
    )


def good_ticker(ticker: Ticker) -> bool:
    return good_dict(
        asdict(ticker),
        [
            "ask",
            "bid",
            "last",
            "low",
            "high",
            "open",
            "volume",
            "volume_quote",
            "timestamp",
        ]
    )


def good_price(price: Price) -> bool:
    return good_dict(
        asdict(price),
        [
            "currency",
            "price",
            "timestamp",
        ]
    )


def good_price_history(price_history: PriceHistory) -> bool:
    good = good_dict(
        asdict(price_history),
        [
            "currency",
            "history"
        ])
    if not good:
        return False
    for history in price_history.history:
        if not good_history(history):
            return False
    return True


def good_ticker_price(price: Price) -> bool:
    return good_dict(
        asdict(price),
        [
            "price",
            "timestamp",
        ]
    )


def good_history(price_history: PricePoint) -> bool:
    return good_dict(
        asdict(price_history),
        [
            "timestamp",
            "open",
            "close",
            "min",
            "max",
        ])


def good_public_trade(trade: PublicTrade) -> bool:
    return good_dict(
        asdict(trade),
        [
            "id",
            "price",
            "qty",
            "side",
            "timestamp",
        ]
    )


def good_orderbook_level(level: OrderBookLevel) -> bool:
    return good_dict(
        asdict(level),
        [
            "price",
            "quantity",
        ]
    )


def good_orderbook(orderbook: OrderBook) -> bool:
    good_orderbook = good_dict(
        asdict(orderbook),
        [
            "timestamp",
            "ask",
            "bid",
        ]
    )
    if not good_orderbook:
        return False

    for level in orderbook.ask:
        if not good_orderbook_level(level):
            return False

    for level in orderbook.bid:
        if not good_orderbook_level(level):
            return False

    return True


def good_candle(candle: Candle) -> bool:
    return good_dict(
        asdict(candle),
        [
            "timestamp",
            "open",
            "close",
            "min",
            "max",
            "volume",
            "volume_quote",
        ]
    )


def good_candle_list(candles: List[Candle]) -> bool:
    for candle in candles:
        if not good_candle(candle):
            return False
    return True


def good_balance(balance: Balance) -> bool:
    return good_dict(
        asdict(balance),
        [
            "currency",
            "available",
            "reserved",
        ]
    )


def good_order(order: Order) -> bool:
    good = good_dict(
        asdict(order),
        [
            "id",
            "client_order_id",
            "symbol",
            "side",
            "status",
            "type",
            "time_in_force",
            "quantity",
            "price",
            "quantity_cumulative",
            "created_at",
            "updated_at",
            # "expire_time",  # optional
            # "stop_price"  # optional
            # "post_only",  # optional
            # "trades",  # optional
            # "original_client_order_id"  # optional
        ]
    )
    if not good:
        return False
    if not order.trades is None:
        if not good_list(good_trade_of_order, order.trades):
            return False
    return True


def good_trade_of_order(trade) -> bool:
    return good_dict(
        asdict(trade),
        [
            "id",
            "quantity",
            "price",
            "fee",
            "taker",
            "timestamp"
        ]
    )


def good_order_list(orders: List[Order]) -> bool:
    for order in orders:
        if not good_order(order):
            return False
    return True


def good_trade(trade: Dict[str, Any]) -> bool:
    return good_dict(
        asdict(trade),
        [
            "id",
            "order_id",
            "client_order_id",
            "symbol",
            "side",
            "quantity",
            "price",
            "fee",
            "timestamp",
        ]
    )


def good_transaction(transaction: Transaction) -> bool:
    good = good_dict(
        asdict(transaction),
        [
            "id",
            "status",
            "type",
            "subtype",
            "created_at",
            "updated_at",
            # "native", # optional
            # "primetrust", # optional
            # "meta" # optional
        ]
    )
    if not good:
        return False
    if not transaction.native is None:
        if not good_native_transaction(transaction.native):
            return False

    if not transaction.meta is None:
        if not good_meta_transaction(transaction.meta):
            return False
    return True


def good_native_transaction(transaction: NativeTransaction) -> bool:
    return good_dict(
        asdict(transaction),
        [
            "tx_id",
            "index",
            "currency",
            "amount",
            # "fee", # optional
            # "address", # optional
            # "payment_id", # optional
            # "hash", # optional
            # "offchain_id", # optional
            # "confirmations", # optional
            # "public_comment", # optional
            # "error_code", # optional
            # "senders" # optional
        ]
    )


def good_meta_transaction(transaction: MetaTransaction) -> bool:
    return good_dict(
        asdict(transaction),
        [
            "fiat_to_crypto",
            "id",
            "provider_name",
            "order_type",
            "order_type",
            "source_currency",
            "target_currency",
            "wallet_address",
            "tx_hash",
            "target_amount",
            "source_amount",
            "status",
            "created_at",
            "updated_at",
            "deleted_at",
            "payment_method_type"
        ]
    )


def good_address(address: Address) -> bool:
    return good_dict(
        asdict(address),
        [
            "address",
            "currency",
            # "payment_id", # optional
            # "public_key" # optional
        ]
    )


def good_trading_commission(commission: Commission) -> bool:
    return good_dict(
        asdict(commission),
        [
            "symbol",
            "take_rate",
            "make_rate",
        ]
    )
