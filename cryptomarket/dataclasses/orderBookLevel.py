from dataclasses import dataclass


@dataclass
class OrderBookLevel:
    price: str
    quantity: str
