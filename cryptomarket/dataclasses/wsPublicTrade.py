from dataclasses import dataclass


@dataclass
class WSPublicTrade:
    t: int = None
    """Timestamp in milliseconds"""
    i: str = None
    """Trade identifier"""
    p: str = None
    """Price"""
    q: str = None
    """Quantity"""
    s: str = None
    """Side"""
