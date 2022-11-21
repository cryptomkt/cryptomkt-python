from dataclasses import dataclass

@dataclass
class Candle:
    timestamp: str = None
    open: str = None
    close: str = None
    min: str = None
    max: str = None
    volume: str = None
    volume_quote: str = None
