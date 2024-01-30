from dataclasses import dataclass
from typing import Any, Dict, List

from cryptomarket.dataclasses.orderBookLevel import OrderBookLevel


@dataclass
class OrderBook:
    timestamp: str
    ask: List[OrderBookLevel]
    bid: List[OrderBookLevel]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        asks = [OrderBookLevel(price=x[0], quantity=x[1]) for x in data['ask']]
        bids = [OrderBookLevel(price=x[0], quantity=x[1]) for x in data['bid']]
        return cls(timestamp=data['timestamp'], ask=asks, bid=bids)
