from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Fee:
    fee: Optional[str]
    network_fee: Optional[str]
    amount: Optional[str]
    currency: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data.get('fee'), data.get('networkFee'), data.get('amount'), data.get('currency'))
