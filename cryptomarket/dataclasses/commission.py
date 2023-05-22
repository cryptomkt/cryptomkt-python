from dataclasses import dataclass
from typing import Optional


@dataclass
class Commission:
    take_rate: str
    make_rate: str
    symbol: Optional[str] = None
