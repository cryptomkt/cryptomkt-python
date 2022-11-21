import time
from dataclasses import asdict
from typing import Any, Dict, List

from cryptomarket.dataclasses import (Balance, OrderBookLevel, Report,
                                      WSCandle, WSMiniTicker, WSOrderBook,
                                      WSOrderBookTop, WSPublicTrade, WSTicker,
                                      WSTrade)
from tests.rest.test_helpers import good_list


def defined(a_dict, key):
    if key not in a_dict:
        return False
    val = a_dict[key]
    if isinstance(val, str) and val == "":
        return False
    return True


def good_dict(a_dict: Dict[str, Any], fields: List[str]) -> bool:
    if not isinstance(a_dict, dict):
        return False
    for field in fields:
        if not defined(a_dict, field):
            return False
    return True


def good_wsticker(ticker: WSTicker) -> bool:
    return good_dict(
        asdict(ticker),
        [
            "t",
            "a",
            "A",
            "b",
            "B",
            "c",
            "o",
            "h",
            "l",
            "v",
            "q",
            "p",
            "P",
            "L",
        ]
    )


def good_mini_ticker(miniticker: WSMiniTicker) -> bool:
    return good_dict(
        asdict(miniticker),
        [
            "t",
            "o",
            "c",
            "h",
            "l",
            "v",
            "q"
        ]
    )


def good_public_trade(trade: WSPublicTrade) -> bool:
    return good_dict(
        asdict(trade),
        [
            "t",
            "i",
            "p",
            "q",
            "s",
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


def good_wsorder_book(orderbook: WSOrderBook) -> bool:
    good_orderbook = good_dict(
        asdict(orderbook),
        [
            "t",
            "s",
            "a",
            "b",
        ]
    )
    if not good_orderbook:
        return False

    for level in orderbook.a:
        if not good_orderbook_level(level):
            return False

    for level in orderbook.b:
        if not good_orderbook_level(level):
            return False

    return True


def good_orderbook_top(orderbook_top: WSOrderBookTop) -> bool:
    return good_dict(
        asdict(orderbook_top),
        [
            "t",
            "a",
            "b",
            "A",
            "B",
        ]
    )


def good_candle(candle: WSCandle) -> bool:
    return good_dict(
        asdict(candle),
        [
            "t",
            "o",
            "c",
            "h",
            "l",
            "v",
            "q",
        ]
    )


def good_candle_list(candles: List[WSCandle]) -> bool:
    for candle in candles:
        if not good_candle(candle):
            return False
    return True


def good_balances(balances: List[Balance]) -> bool:
    for balance in balances:
        good_balance = good_dict(
            asdict(balance),
            [
                "currency",
                "available",
                "reserved",
            ]
        )
        if not good_balance:
            return False
    return True


def good_wstrade(trade: WSTrade) -> bool:
    return good_dict(
        asdict(trade),
        [
            't',
            'i',
            'p',
            'q',
            's',
        ]
    )


def good_report(report: Report):
    return good_dict(
        asdict(report),
        [
            'id',
            'client_order_id',
            'symbol',
            'side',
            'status',
            'type',
            'time_in_force',
            'quantity',
            'price',
            'cum_quantity',
            'post_only',
            'created_at',
            'updated_at',
            'stop_price',
            'expire_time',
            'original_client_order_id',
            # 'trade_id',
            # 'trade_quantity',
            # 'trade_price',
            # 'trade_fee',
            # 'trade_taker',
            # 'report_type',
            # 'order_list_id',
            # 'contingency_type',
        ]
    )


def good_report_list(report_list: List[Report]):
    return good_list(good_report, report_list)


class Veredict:
    failed = False
    message = ''
    done = False

    @classmethod
    def fail(cls, message):
        cls.failed = True
        cls.message = message
        cls.done = True

    @classmethod
    def reset(cls):
        cls.failed = False
        cls.message = ''
        cls.done = False

    @classmethod
    def wait_done(cls):
        while not cls.done:
            time.sleep(1)
