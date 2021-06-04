from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Union

from cryptomarket.exceptions import ArgumentFormatException


class CHECKER(str, Enum):
    @classmethod
    def check_value(cls, value):
        if value not in cls._value2member_map_:
            raise ArgumentFormatException(f'invalid {cls.__name__} argument.', [item.value for item in cls])

class SORT(CHECKER):
    ASCENDING = 'ASC'
    DESCENDING = 'DESC'

class BY(CHECKER):
    TIMESTAMP = 'timestamp'
    ID = 'id'

class PERIOD(CHECKER):
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

class SIDE(CHECKER):
    BUY = 'buy'
    SELL = 'sell'

class ORDER_TYPE(CHECKER):
    LIMIT = 'limit'
    MARKET = 'market'
    STOPLIMIT = 'stopLimit'
    STOPMARKET = 'stopMarket'

class TIME_IN_FORCE(CHECKER):
    GTC = 'GTC' # Good till canceled
    IOC = 'IOC' # Immediate or cancell
    FOK = 'FOK' # Fill or kill
    DAY = 'Day' # Good for the day
    GTD = 'GDT' # Good till date

class TRANSFER_TYPE(CHECKER):
    BANK_TO_EXCHANGE = 'bankToExchange',
    EXCHANGE_TO_BANK = 'exchangeToBank'

class TRANSFER_BY(CHECKER):
    USERNAME = 'username',
    EMAIL = 'email'

class DictBuilder:
    def __init__(self):
        self.the_dict = dict()
    
    def build(self):
        return self.the_dict.copy()
    
    def addList(self, key, val:List[str]):
        if val is not None:
            query = ','.join(val)
            if isinstance(val, str):
                query = val
            self.the_dict[key] = query
        return self

    def add(self, key, val):
        if val is not None:
            self.the_dict[key] = val
        return self

    def currencies(self, val: List[str]):
        self.addList("currencies", val)
        return self

    def symbols(self, val: List[str]):
        self.addList("symbols", val)
        return self
        
    def currency(self, val: str):
        self.add("currency", val)
        return self
    
    def symbol(self, val: str):
        self.add("symbol", val)
        return self
    
    def period(self, val: str):
        if val is not None:
            PERIOD.check_value(val)
            self.the_dict['period'] = val
        return self
    
    def sort(self, val: str):
        if val is not None:
            SORT.check_value(val)
            self.the_dict['sort'] = val
        return self

    def by(self, val: str):
        if val is not None:
            BY.check_value(val)
            self.the_dict['by'] = val   
        return self    
    
    def since(self, val: str):
        self.add("from", val)
        return self
    
    def till(self, val: str):
        self.add("till", val)
        return self

    def limit(self, val: int):
        self.add("limit", val)
        return self

    def offset(self, val: int):
        self.add("offset", val)
        return self

    def volume(self, val: str):
        self.add("volume", val)
        return self

    def side(self, val: str):
        if val is not None:
            SIDE.check_value(val)
            self.the_dict["side"] = val
        return self
        
    def order_type(self, val: str):
        if val is not None:
            ORDER_TYPE.check_value(val)
            self.the_dict['type'] = val
        return self

    def quantity(self, val: str):
        self.add("quantity", val)
        return self
    
    def price(self, val: str):
        self.add("price", val)
        return self

    def stop_price(self, val: str):
        self.add("stopPrice", val)
        return self

    def time_in_force(self, val: str):
        if val is not None:
            TIME_IN_FORCE.check_value(val)
            self.the_dict["timeInForce"] = val
        return self
        
    def expire_time(self, val: str):
        self.add("expireTime", val)
        return self

    def strict_validate(self, val: bool):
        self.add("strictValidate", val)
        return self
    
    def post_only(self, val: bool):
        self.add("postOnly", val)
        return self

    def client_order_id(self, val: str):
        self.add("clientOrderId", val)
        return self

    def wait(self, val: int):
        self.add("wait", val)
        return self

    def margin(self, val: str):
        self.add("margin", val)
        return self

    def address(self, val: str):
        self.add("address", val)
        return self

    def amount(self, val: str):
        self.add("amount", val)
        return self
    
    def payment_id(self, val: str):
        self.add("paymentId", val)
        return self
    
    def include_fee(self, val: str):
        self.add("includeFee", val)
        return self
    
    def auto_commit(self, val: str):
        self.add("autoCommit", val)
        return self
    
    def from_currency(self, val: str):
        self.add("fromCurrency", val)
        return self
    
    def to_currency(self, val: str):
        self.add("toCurrency", val)
        return self

    def transfer_type(self, val: str):
        if val is not None:
            TRANSFER_TYPE.check_value(val)
            self.the_dict["type"] = val
        return self

    def transfer_by(self, val: str):
        if val is not None:
            TRANSFER_BY.check_value(val)
            self.the_dict["by"] = val
        return self
        
    def identifier(self, val: str):
        self.add("identifier", val)
        return self

    def show_senders(self, val: bool):
        self.add("showSenders", val)
        return self

    def request_client_id(self, val: str):
        self.add("requestClientId", val)
        return self
