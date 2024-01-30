from dataclasses import dataclass

@dataclass
class Candle:
    timestamp: str
    open: str
    close: str
    min: str
    max: str
    volume: str
    volume_quote: str
