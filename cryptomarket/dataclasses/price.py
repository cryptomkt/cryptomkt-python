from dataclasses import dataclass
from typing import Optional


@dataclass
class Price:
    timestamp: str
    price: Optional[str] = None
    currency: Optional[str] = None
