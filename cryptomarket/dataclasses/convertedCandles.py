from dataclasses import dataclass
from typing import Dict, List
from cryptomarket.dataclasses.candle import Candle


@dataclass
class ConvertedCandles:
    target_currency: str
    data: Dict[str, List[Candle]]
