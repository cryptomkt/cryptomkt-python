from dataclasses import dataclass


@dataclass
class WSPublicTrade:
    t: int
    """Timestamp in milliseconds"""
    i: str
    """Trade identifier"""
    p: str
    """Price"""
    q: str
    """Quantity"""
    s: str
    """Side"""
