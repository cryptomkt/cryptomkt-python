from dataclasses import dataclass
from typing import Optional


@dataclass
class Balance:
    available: str
    reserved: str
    currency: Optional[str] = None
