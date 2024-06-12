from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Fee:
    fee: str
    network_fee: Optional[str]
    amount: str
    currency: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data['fee'], data.get('networkFee'), data['amount'], data['currency'])
