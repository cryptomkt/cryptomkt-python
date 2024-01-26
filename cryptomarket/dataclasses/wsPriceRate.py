from dataclasses import dataclass


@dataclass
class WSPriceRate:
    t: int
    """Timestamp in milliseconds"""
    r: str
    """rate"""