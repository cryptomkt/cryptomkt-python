from dataclasses import dataclass, field
from typing import List

from cryptomarket.dataclasses.balance import Balance


@dataclass
class SubAccountBalance:
    wallet: List[Balance] = field(default_factory=list)
    spot: List[Balance] = field(default_factory=list)
