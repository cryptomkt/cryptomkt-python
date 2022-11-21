from dataclasses import dataclass


@dataclass
class WSTrade:
    t: int = None
    """Timestamp in milliseconds"""
    i: int = None
    """Trade identifier"""
    p: str = None
    """Price"""
    q: str = None
    """Quantity"""
    s: str = None
    """Side"""
