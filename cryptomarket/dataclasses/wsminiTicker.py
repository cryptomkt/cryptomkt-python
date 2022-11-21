from dataclasses import dataclass


@dataclass
class WSMiniTicker:
    t: int = None
    """Timestamp in milliseconds"""
    o: str = None
    """Open price"""
    c: str = None
    """Last price"""
    h: str = None
    """High price"""
    l: str = None
    """Low price"""
    v: str = None
    """Base asset volume"""
    q: str = None
    """Quote asset volume"""
