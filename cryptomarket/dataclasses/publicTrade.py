from dataclasses import dataclass


@dataclass
class PublicTrade:
    id: int
    price: str
    qty: str
    side: str
    timestamp: str
