from dataclasses import dataclass, field
from typing import Any, Dict, List

from dacite import from_dict

from cryptomarket.dataclasses.orderBookLevel import OrderBookLevel


@dataclass
class WSOrderBook:
    t: int = None
    """Timestamp in milliseconds"""
    s: int = None
    """Sequence number"""
    a: List[OrderBookLevel] = field(default_factory=list)
    """asks"""
    b: List[OrderBookLevel] = field(default_factory=list)
    "bids"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        asks = [
            from_dict(data_class=OrderBookLevel, data={'price': x[0], 'quantity':x[1]}) for x in data['a']
        ]
        bids = [
            from_dict(data_class=OrderBookLevel, data={'price': x[0], 'quantity':x[1]}) for x in data['b']
        ]
        return cls(
            t=int(data['t']),
            s=int(data['s']),
            a=asks,
            b=bids,
        )
