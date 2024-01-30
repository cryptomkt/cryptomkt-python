from dataclasses import dataclass
from typing import List

from cryptomarket.dataclasses.pricePoint import PricePoint


@dataclass
class PriceHistory:
    currency: str
    history: List[PricePoint]
