from dataclasses import dataclass
from typing import Optional


@dataclass
class AmountLock:
    id: int
    currency: str
    amount: str
    date_end: str
    description: str
    cancelled: bool
    created_at: str
    cancelled_at: Optional[str] = None
    cancel_description: Optional[str] = None
