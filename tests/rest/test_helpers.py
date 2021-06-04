from typing import Dict, Any, List


# defined checks if a key is present in a dict, and if its value is str, checks if its defined.
# return false when the key is not present or when the value is an empty string, return true otherwise.
def defined(a_dict, key):
    if key not in a_dict: return False
    val = a_dict[key]
    if isinstance(val, str) and val == "": return False
    return True

# good_dict checks all of the values in the fields list to be present in the dict, and if they are 
# present, check the defined() condition to be true. if any of the fields fails to be defined(), then 
# this function returns false
def good_dict(a_dict: Dict[str, Any], fields: List[str]) -> bool:
    if not isinstance(a_dict, dict): return False
    for field in fields:
        if not defined(a_dict, field): return False
    return True


# good_currency checks the precence of every field in the currency dict
def good_currency(currency: Dict[str, Any]) -> bool:
    return good_dict(currency,
        [
            "id",
            "fullName",
            "crypto",
            "payinEnabled",
            "payinPaymentId",
            "payinConfirmations",
            "payoutEnabled",
            "payoutIsPaymentId",
            "transferEnabled",
            "delisted",
            # "precisionPayout",
            # "precisionTransfer",
        ]
    )

# good_symbol check the precence of every field in the symbol dict
def good_symbol(symbol: Dict[str, Any]) -> bool:
    return good_dict(symbol, 
        [
            'id',
            'baseCurrency',
            'quoteCurrency',
            'quantityIncrement',
            'tickSize',
            'takeLiquidityRate',
            'provideLiquidityRate',
            # 'feeCurrency'
        ]
    )


# good_ticker check the precence of every field in the ticker dict
def good_ticker(ticker: Dict[str, Any]) -> bool:
    return good_dict(ticker, 
        [
            "symbol",
            "ask",
            "bid",
            "last",
            "low",
            "high",
            "open",
            "volume",
            "volumeQuote",
            "timestamp",
        ]
    )


# good_public_trade check the precence of every field in the trade dict
def good_public_trade(trade: Dict[str, Any]) -> bool:
    return good_dict(trade, 
        [
            "id",
            "price",
            "quantity",
            "side",
            "timestamp",
        ]
    )

# good_orderbook_level check the precence of every field in the level dict
def good_orderbook_level(level: Dict[str, Any]) -> bool:
    return good_dict(level, 
        [
            "price",
            "size",
        ]
    )

# good_orderbook check the precence of every field in the orderbook dict
# and the fields of each level in each side of the orderbook
def good_orderbook(orderbook: Dict[str, Any]) -> bool:
    good_orderbook = good_dict(orderbook, 
        [
            "symbol",
            "timestamp",
            "batchingTime",
            "ask",
            "bid",
        ]
    )
    if not good_orderbook: return False

    for level in orderbook["ask"]:
        if not good_orderbook_level(level): return False

    for level in orderbook["bid"]:
        if not good_orderbook_level(level): return False

    return True



# good_candle check the precence of every field in the candle dict
def good_candle(candle: Dict[str, Any]) -> bool:
    return good_dict(candle, 
        [
            "timestamp",
            "open",
            "close",
            "min",
            "max",
            "volume",
            "volumeQuote",
        ]
    )


# good_candle_list check the precence of every field of the candle dict in every candle of the candle list.
def good_candle_list(candles: List[Dict[str, Any]]) -> bool:
    for candle in candles:
        if not good_candle(candle): return False
    return True


# good_balances check the precence of every field on every balance dict
def good_balances(balances: List[Dict[str, Any]]) -> bool:
    for balance in balances:
        good_balance = good_dict(balance, 
            [
                "currency",
                "available",
                "reserved",
            ]
        )
        if not good_balance: return False
    return True


# good_order check the precence of every field in the order dict
def good_order(order: Dict[str, Any]) -> bool:
    return good_dict(order, 
        [
            "id",
            "clientOrderId",
            "symbol",
            "side",
            "status",
            "type",
            "timeInForce",
            "quantity",
            "price",
            "cumQuantity",
            # "postOnly", # does not appears in the orders in orders history
            "createdAt",
            "updatedAt",
        ]
    )


# good_order_list check the precence of every field of the order dict in every order of the order list.
def good_order_list(orders: List[Dict[str, Any]]) -> bool:
    for order in orders:
        if not good_order(order): return False
    return True

# good_trade check the precence of every field in the trade dict
def good_trade(trade: Dict[str, Any]) -> bool:
    return good_dict(trade, 
        [
            "id",
            "orderId",
            "clientOrderId",
            "symbol",
            "side",
            "quantity",
            "price",
            "fee",
            "timestamp",
        ]
    )



# good_transaction check the precence of every field in the transaction dict
def good_transaction(transaction: Dict[str, Any]) -> bool:
    return good_dict(transaction, 
        [
            "id",
            "index",
            "currency",
            "amount",
            # "fee",
            # "address",
            # "hash",
            "status",
            "type",
            "createdAt",
            "updatedAt",
        ]
    )