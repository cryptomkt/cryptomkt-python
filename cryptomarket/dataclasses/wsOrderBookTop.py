from dataclasses import dataclass


@dataclass
class WSOrderBookTop:
    t: int = None
    """Timestamp in milliseconds"""
    a: str = None
    """Best ask"""
    A: str = None
    """Best ask quantity"""
    b: str = None
    """Best bid"""
    B: str = None
    """Best bid quantity"""
