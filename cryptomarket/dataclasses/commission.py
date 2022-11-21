from dataclasses import dataclass


@dataclass
class Commission:
    symbol: str = None
    take_rate: str = None
    make_rate: str = None
