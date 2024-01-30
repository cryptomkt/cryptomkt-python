from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    address: str
    currency: str
    payment_id: Optional[str] = None
    public_key: Optional[str] = None
