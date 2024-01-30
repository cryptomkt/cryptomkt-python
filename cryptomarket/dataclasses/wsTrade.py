from dataclasses import dataclass


@dataclass
class WSTrade:
    t: int
    """Timestamp in milliseconds"""
    i: int
    """Trade identifier"""
    p: str
    """Price"""
    q: str
    """Quantity"""
    s: str
    """Side"""
