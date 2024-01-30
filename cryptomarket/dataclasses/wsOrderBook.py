from dataclasses import dataclass
from typing import Any, Dict, List

from cryptomarket.dataclasses.orderBookLevel import OrderBookLevel


@dataclass
class WSOrderBook:
    t: int
    """Timestamp in milliseconds"""
    s: int
    """Sequence number"""
    a: List[OrderBookLevel]
    """asks"""
    b: List[OrderBookLevel]
    "bids"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        asks = [OrderBookLevel(price=x[0], quantity=x[1]) for x in data['a']]
        bids = [OrderBookLevel(price=x[0], quantity=x[1]) for x in data['b']]
        return cls(t=int(data['t']), s=int(data['s']), a=asks, b=bids)
