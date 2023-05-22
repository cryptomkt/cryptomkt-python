from dataclasses import dataclass


@dataclass
class WSOrderBookTop:
    t: int
    """Timestamp in milliseconds"""
    a: str
    """Best ask"""
    A: str
    """Best ask quantity"""
    b: str 
    """Best bid"""
    B: str
    """Best bid quantity"""
