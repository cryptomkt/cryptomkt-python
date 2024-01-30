from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from cryptomarket.exceptions import ArgumentFormatException


class Checker(str, Enum):
    @classmethod
    def check_value(cls, value):
        if value not in cls._value2member_map_:
            raise ArgumentFormatException(f'invalid {cls.__name__} argument.', [
                                          item.value for item in cls])


class TransferType(Checker):
    TO_SUB_ACCOUNT = 'to_sub_account'
    FROM_SUB_ACCOUNT = 'from_sub_account'


class ContingencyType(Checker):
    ALL_OR_NONE = "allOrNone"
    AON = "allOrNone"
    ONE_CANCEL_OTHER = "oneCancelOther"
    OCO = "oneCancelOther"
    ONE_TRIGGER_OTHER = "oneTriggerOther"
    OTO = "oneTriggerOther"
    ONE_TRIGGER_ONE_CANCEL_OTHER = "oneTriggerOneCancelOther"
    OTOCO = "oneTriggerOneCancelOther"


class Sort(Checker):
    ASCENDING = 'ASC'
    DESCENDING = 'DESC'


class Period(Checker):
    _1_MINS = 'M1'
    _3_MINS = 'M3'
    _5_MINS = 'M5'
    _15_MINS = 'M15'
    _30_MINS = 'M30'
    _1_HOURS = 'H1'
    _4_HOURS = 'H4'
    _1_DAYS = 'D1'
    _7_DAYS = 'D7'
    _1_MONTHS = '1M'


class Side(Checker):
    BUY = 'buy'
    SELL = 'sell'


class OrderStatus(Checker):
    NEW = 'new'
    SUSPENDED = 'suspended'
    PARTIALLY_FILLED = 'partiallyFilled'
    FILLED = 'filled'
    CANCELED = 'canceled'
    EXPIRED = 'expired'


class OrderType(Checker):
    LIMIT = 'limit'
    MARKET = 'market'
    STOP_LIMIT = 'stopLimit'
    STOP_MARKET = 'stopMarket'
    TAKE_PROFIT_LIMIT = 'takeProfitLimit'
    TAKE_PROFIT_MARKET = 'takeProfitMarket'


class TimeInForce(Checker):
    GTC = 'GTC'  # Good till canceled
    IOC = 'IOC'  # Immediate or cancell
    FOK = 'FOK'  # Fill or kill
    DAY = 'Day'  # Good for the day
    GTD = 'GDT'  # Good till date


class IdentifyBy(Checker):
    USERNAME = 'username'
    EMAIL = 'email'


class Offchain(Checker):
    NEVER = 'never'
    OPTIONALLY = 'optionally'
    REQUIRED = 'required'


class Account(Checker):
    SPOT = 'spot'
    WALLET = 'wallet'


class TickerSpeed(Checker):
    _1_SECOND = '1s'
    _3_SECONDS = '3s'


class PriceRateSpeed(Checker):
    _1_SECOND = '1s'
    _3_SECONDS = '3s'


class OrderbookSpeed(Checker):
    _100_MILISECONDS = '100ms'
    _500_MILISECONDS = '500ms'
    _1000_MILISECONDS = '1000ms'


class TransactionType(Checker):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    TRANSFER = 'TRANSFER'
    SAWAP = 'SAWAP'


class TransactionSubType(Checker):
    UNCLASSIFIED = 'UNCLASSIFIED'
    BLOCKCHAIN = 'BLOCKCHAIN'
    AIRDROP = 'AIRDROP'
    AFFILIATE = 'AFFILIATE'
    STAKING = 'STAKING'
    BUY_CRYPTO = 'BUY_CRYPTO'
    OFFCHAIN = 'OFFCHAIN'
    FIAT = 'FIAT'
    SUB_ACCOUNT = 'SUB_ACCOUNT'
    WALLET_TO_SPOT = 'WALLET_TO_SPOT'
    SPOT_TO_WALLET = 'SPOT_TO_WALLET'
    WALLET_TO_DERIVATIVES = 'WALLET_TO_DERIVATIVES'
    DERIVATIVES_TO_WALLET = 'DERIVATIVES_TO_WALLET'
    CHAIN_SWITCH_FROM = 'CHAIN_SWITCH_FROM'
    CHAIN_SWITCH_TO = 'CHAIN_SWITCH_TO'
    INSTANT_EXCHANGE = 'INSTANT_EXCHANGE'


class TransactionStatus(Checker):
    CREATED = 'CREATED'
    PENDING = 'PENDING'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'
    ROLLED_BACK = 'ROLLED_BACK'


class SortBy(Checker):
    TIMESTAMP = "timestamp"
    CREATED_AT = 'created_at'
    ID = 'id'


class Depth(Checker):
    _5 = 'D5'
    _10 = 'D10'
    _20 = 'D20'


class SubscriptionMode(Checker):
    UPDATES = "updates"
    BATCHES = "batches"


@dataclass
class OrderRequest:
    symbol: str
    side: Side
    quantity: str
    client_order_id: Optional[str] = None
    type: Optional[OrderType] = None
    time_in_force: Optional[TimeInForce] = None
    price: Optional[str] = None
    expire_time: Optional[str] = None
    stop_price: Optional[str] = None
    strict_validate: Optional[bool] = None
    post_only: Optional[bool] = None
    take_rate: Optional[str] = None
    make_rate: Optional[str] = None


@dataclass
class FeeRequest:
    currency: str
    amount: str
    network_code: Optional[str] = None


@dataclass
class ACLSettings:
    sub_account_id: str = None
    deposit_address_generation_enabled: bool = None
    withdraw_enabled: bool = None
    description: str = None
    created_at: str = None
    updated_at: str = None


def clean_nones(a_dict: Dict[Any, Optional[Any]]) -> Dict[Any, Any]:
    return {k: v for k, v in a_dict.items() if v is not None}


class DictBuilder:
    def __init__(self):
        self.the_dict = dict()

    def build(self):
        orderedDict = dict()
        for parameter in sorted(self.the_dict):
            orderedDict[parameter] = self.the_dict[parameter]
        return orderedDict

    def add_coma_separated_list(self, key, val: List[str]):
        if val is not None:
            query = ','.join(val)
            if isinstance(val, str):
                query = val
            self.the_dict[key] = query
        return self

    def add_coma_separated_list_checking(self, checker: Checker, key, val: List[str]):
        if val is not None:
            for element in val:
                checker.check_value(element)
            query = ','.join(val)
            if isinstance(val, str):
                query = val
            self.the_dict[key] = query
        return self

    def add(self, key, val):
        if val is not None:
            self.the_dict[key] = val
        return self

    def add_cheking(self, checker: Checker, key, val):
        if val is not None:
            checker.check_value(val)
            self.the_dict[key] = val
        return self

    def currencies(self, val: List[str]):
        return self.add_coma_separated_list("currencies", val)

    def symbols(self, val: List[str]):
        return self.add_coma_separated_list("symbols", val)

    def currency(self, val: str):
        return self.add("currency", val)

    def from_(self, val: str):
        return self.add("from", val)

    def to(self, val: str):
        return self.add("to", val)

    def symbol(self, val: str):
        return self.add("symbol", val)

    def period(self, val: str):
        return self.add_cheking(Period, 'period', val)

    def sort(self, val: str):
        return self.add_cheking(Sort, 'sort', val)

    def since(self, val: str):
        return self.add("from", val)

    def until(self, val: str):
        return self.add("until", val)

    def till(self, val: str):
        return self.add("till", val)

    def limit(self, val: int):
        return self.add("limit", val)

    def offset(self, val: int):
        return self.add("offset", val)

    def by(self, val: str):
        return self.add("by", val)

    def volume(self, val: str):
        return self.add("volume", val)

    def side(self, val: str):
        return self.add_cheking(Side, 'side', val)

    def order_type(self, val: str):
        return self.add_cheking(OrderType, 'type', val)

    def quantity(self, val: str):
        return self.add("quantity", val)

    def price(self, val: str):
        return self.add("price", val)

    def stop_price(self, val: str):
        return self.add("stop_price", val)

    def time_in_force(self, val: str):
        return self.add_cheking(TimeInForce, 'time_in_force', val)

    def expire_time(self, val: str):
        return self.add("expire_time", val)

    def strict_validate(self, val: bool):
        return self.add("strict_validate", val)

    def post_only(self, val: bool):
        return self.add("post_only", val)

    def client_order_id(self, val: str):
        return self.add("client_order_id", val)

    def new_client_order_id(self, val: str):
        return self.add("new_client_order_id", val)

    def wait(self, val: int):
        return self.add("wait", val)

    def margin(self, val: str):
        return self.add("margin", val)

    def address(self, val: str):
        return self.add("address", val)

    def amount(self, val: str):
        return self.add("amount", val)

    def payment_id(self, val: str):
        return self.add("paymentId", val)

    def include_fee(self, val: str):
        return self.add("include_fee", val)

    def auto_commit(self, val: str):
        return self.add("auto_commit", val)

    def _from(self, val: str):
        return self.add("from", val)

    def from_currency(self, val: str):
        return self.add("from_currency", val)

    def to_currency(self, val: str):
        return self.add("to_currency", val)

    def source(self, val: str):
        return self.add_cheking(Account, "source", val)

    def destination(self, val: str):
        return self.add_cheking(Account, "destination", val)

    def identify_by(self, val: str):
        return self.add_cheking(IdentifyBy, 'by', val)

    def identifier(self, val: str):
        return self.add("identifier", val)

    def show_senders(self, val: bool):
        return self.add("show_senders", val)

    def request_client_id(self, val: str):
        return self.add("request_client_id", val)

    def depth(self, val: str):
        return self.add("depth", val)

    def speed(self, val: str):
        return self.add("speed", val)

    def make_rate(self, val: str):
        return self.add("make_rate", val)

    def take_rate(self, val: str):
        return self.add("take_rate", val)

    def order_id(self, val: str):
        return self.add("order_id", val)

    def use_offchain(self, val: str):
        return self.add_cheking(Offchain, 'use_offchain', val)

    def public_comment(self, val: str):
        return self.add("public_comment", val)

    def symbols_as_list(self, val: List[str]):
        return self.add('symbols', val)

    def currencies_as_list(self, val: List[str]):
        return self.add('currencies', val)

    def transaction_type(self, val: List[str]):
        return self.add_cheking(TransactionType, 'type', val)

    def transaction_types(self, val: List[str]):
        return self.add_coma_separated_list_checking(TransactionType, 'types', val)

    def transaction_subtype(self, val: str):
        return self.add_cheking(TransactionSubType, 'subtype', val)

    def transaction_subtypes(self, val: str):
        return self.add_coma_separated_list_checking(TransactionSubType, 'subtypes', val)

    def transaction_statuses(self, val: str):
        return self.add_coma_separated_list_checking(TransactionStatus, 'statuses', val)

    def id_from(self, val: str):
        return self.add('id_from', val)

    def id_till(self, val: str):
        return self.add('id_till', val)

    def tx_ids(self, val: List[str]):
        return self.add_coma_separated_list('tx_ids', val)

    # TODO: choose one, sort_by or order_by, and make it constant throughout the sdk.
    def sort_by(self, val: str):
        return self.add_cheking(SortBy, 'order_by', val)

    def base_currency(self, val: str):
        return self.add('base_currency', val)

    def active_at(self, val: str):
        return self.add('active_at', val)

    def transaction_id(self, val: str):
        return self.add('transaction_id', val)

    def active(self, val: bool):
        return self.add('active', val)

    def order_list_id(self, val: str):
        return self.add('order_list_id', val)

    def contingency_type(self, val: str):
        return self.add_cheking(ContingencyType, 'contingency_type', val)

    def orders(self, val: List[OrderRequest]):
        return self.add('orders', [clean_nones(asdict(order)) for order in val])

    def sub_account_ids(self, val: List[str]):
        return self.add_coma_separated_list('sub_account_ids', val)

    def sub_account_id(self, val: str):
        return self.add('sub_account_id', val)

    def subscription_mode(self, val: str):
        return self.add_cheking(SubscriptionMode, 'mode', val)

    def target_currency(self, val: str):
        return self.add('target_currency', val)

    def preferred_network(self, val: str):
        return self.add('preferred_network', val)

    def type(self, val: str):
        return self.add('type', val)

    def acl_settings(self, val: ACLSettings):
        self.add(
            'deposit_address_generation_enabled',
            val.deposit_address_generation_enabled
        )
        self.add('withdraw_enabled', val.withdraw_enabled)
        self.add('description', val.description)
        self.add('created_at', val.created_at)
        return self.add('updated_at', val.updated_at)
