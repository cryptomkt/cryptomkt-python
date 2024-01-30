from dataclasses import dataclass
from typing import Optional


@dataclass
class Ticker:
    timestamp: str
    high: str
    low: str
    volume: str
    volume_quote: str
    ask: Optional[str] = None
    bid: Optional[str] = None
    open: Optional[str] = None
    last: Optional[str] = None
