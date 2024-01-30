from dataclasses import dataclass


@dataclass
class WSMiniTicker:
    t: int
    """Timestamp in milliseconds"""
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
