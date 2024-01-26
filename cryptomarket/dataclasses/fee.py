from dataclasses import dataclass
from typing import Any, Dict, List

from cryptomarket.dataclasses.orderBookLevel import OrderBookLevel


@dataclass
class Fee:
    fee: str
    network_fee: str
    amount: str
    currency: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data.get('fee'), data.get('networkFee'), data.get('amount'), data.get('currency'))
