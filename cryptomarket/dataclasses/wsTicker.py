from dataclasses import dataclass


@dataclass
class WSTicker:
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
    c: str
    """Last price"""
    o: str
    """Open price"""
    h: str
    """High price"""
    l: str
    """Low price"""
    v: str
    """Base asset volume"""
    q: str
    """Quote asset volume"""
    p: str
    """Price change"""
    P: str
    """Price change percent"""
    L: int
    """Last trade identifier"""
