from dataclasses import dataclass


@dataclass
class Trade:
    id: int
    order_id: str
    client_order_id: str
    symbol: str
    side: str
    quantity: str
    price: str
    fee: str
    timestamp: str
    taker: bool
