from dataclasses import dataclass
from typing import Optional


@dataclass
class Ticker:
    timestamp: Optional[str] = None
    ask: Optional[str] = None
    bid: Optional[str] = None
    open: Optional[str] = None
    last: Optional[str] = None
    high: Optional[str] = None
    low: Optional[str] = None
    volume: Optional[str] = None
    volume_quote: Optional[str] = None
