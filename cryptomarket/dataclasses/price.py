from dataclasses import dataclass
from typing import Optional


@dataclass
class Price:
    price: str
    timestamp: str
    currency: Optional[str] = None
