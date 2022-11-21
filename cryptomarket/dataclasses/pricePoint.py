from dataclasses import dataclass


@dataclass
class PricePoint:
    timestamp: str = None
    open: str = None
    close: str = None
    min: str = None
    max: str = None