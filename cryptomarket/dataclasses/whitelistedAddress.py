from dataclasses import dataclass
from typing import Optional


@dataclass
class WhitelistedAddress:
    address: str
    currency: str
    name: str
    network: str
