from dataclasses import dataclass


@dataclass
class Symbol:
    type: str = None
    base_currency: str = None
    quote_currency: str = None
    status: str = None
    quantity_increment: str = None
    tick_size: str = None
    take_rate: str = None
    make_rate: str = None
    fee_currency: str = None
    margin_trading: bool = None
    max_initial_leverage: str = None
