from dataclasses import dataclass


@dataclass
class Price:
    currency: str = None
    price: str = None
    timestamp: str = None