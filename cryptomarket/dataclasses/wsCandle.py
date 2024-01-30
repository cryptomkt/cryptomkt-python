from dataclasses import dataclass


@dataclass
class WSCandle:
    t: int
    """Message timestamp"""
    o: str
    """Open price"""
    c: str
    """Last price"""
    h: str
    """High price"""
    l: str
    """Low price"""
    v: str
    """Base asset volume"""
    q: str
    """Quote asset volume"""
