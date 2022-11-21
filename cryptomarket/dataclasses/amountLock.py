from dataclasses import dataclass


@dataclass
class AmountLock:
    id: int = None
    currency: str = None
    amount: str = None
    date_end: str = None
    description: str = None
    cancelled: bool = None
    cancelled_at: str = None
    cancel_description: str = None
    created_at: str = None
