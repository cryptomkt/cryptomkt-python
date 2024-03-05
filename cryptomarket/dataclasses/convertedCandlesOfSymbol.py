from dataclasses import dataclass
from typing import List

from cryptomarket.dataclasses.candle import Candle


@dataclass
class ConvertedCandlesOfSymbol:
    target_currency: str
    data: List[Candle]
