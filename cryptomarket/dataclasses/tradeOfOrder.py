from dataclasses import dataclass


@dataclass
class TradeOfOrder:
    id: int = None
    quantity: str = None
    price: str = None
    fee: str = None
    taker: bool = None
    timestamp: str = None
