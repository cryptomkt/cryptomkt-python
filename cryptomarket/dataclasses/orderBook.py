from dataclasses import dataclass, field
from typing import Any, Dict, List

from dacite import from_dict

from cryptomarket.dataclasses.orderBookLevel import OrderBookLevel


@dataclass
class OrderBook:
    timestamp: str = None
    ask: List[OrderBookLevel] = field(default_factory=list)
    bid: List[OrderBookLevel] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        asks = [
            from_dict(data_class=OrderBookLevel, data={'price': x[0], 'quantity':x[1]}) for x in data['ask']
        ]
        bids = [
            from_dict(data_class=OrderBookLevel, data={'price': x[0], 'quantity':x[1]}) for x in data['bid']
        ]
        return cls(
            timestamp=data['timestamp'],
            ask=asks,
            bid=bids,
        )
