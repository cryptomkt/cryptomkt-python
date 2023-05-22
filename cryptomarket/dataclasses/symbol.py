from dataclasses import dataclass
from enum import Enum


class SymbolStatus(str, Enum):
    WORKING = 'working'
    SUSPENDED = 'suspended'


@dataclass
class Symbol:
    type: str
    base_currency: str
    quote_currency: str
    status: SymbolStatus
    quantity_increment: str
    tick_size: str
    take_rate: str
    make_rate: str
    fee_currency: str
