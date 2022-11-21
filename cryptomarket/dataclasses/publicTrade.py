from dataclasses import dataclass


@dataclass
class PublicTrade:
    id: int = None
    price: str = None
    qty: str = None
    side: str = None
    timestamp: str = None
