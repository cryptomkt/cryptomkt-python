from dataclasses import dataclass


@dataclass
class Trade:
    id: int = None
    order_id: str = None
    client_order_id: str = None
    symbol: str = None
    side: str = None
    quantity: str = None
    price: str = None
    fee: str = None
    timestamp: str = None
    taker: bool = None
