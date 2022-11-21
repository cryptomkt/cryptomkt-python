from dataclasses import dataclass


@dataclass
class Balance:
    currency: str = None
    available: str = None
    reserved: str = None
    reserved_margin: str = None
