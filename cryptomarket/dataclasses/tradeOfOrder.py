from dataclasses import dataclass


@dataclass
class TradeOfOrder:
    id: int
    quantity: str
    price: str
    fee: str
    taker: bool
    timestamp: str
