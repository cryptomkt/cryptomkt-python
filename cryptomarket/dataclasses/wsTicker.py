from dataclasses import dataclass


@dataclass
class WSTicker:
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
    c: str = None
    """Last price"""
    o: str = None
    """Open price"""
    h: str = None
    """High price"""
    l: str = None
    """Low price"""
    v: str = None
    """Base asset volume"""
    q: str = None
    """Quote asset volume"""
    p: str = None
    """Price change"""
    P: str = None
    """Price change percent"""
    L: int = None
    """Last trade identifier"""
