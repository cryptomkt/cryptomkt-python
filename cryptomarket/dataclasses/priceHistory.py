from dataclasses import dataclass, field
from typing import List

from cryptomarket.dataclasses.pricePoint import PricePoint


@dataclass
class PriceHistory:
    currency: str = None
    history: List[PricePoint] = field(default_factory=list)
