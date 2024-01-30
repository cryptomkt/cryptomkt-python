from dataclasses import dataclass


@dataclass
class PricePoint:
    timestamp: str
    open: str
    close: str
    min: str
    max: str