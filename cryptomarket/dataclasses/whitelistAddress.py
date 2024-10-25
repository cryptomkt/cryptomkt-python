from dataclasses import dataclass
from typing import Optional


@dataclass
class WhitelistAddress:
    address: str
    currency: str
    name: str
    network: str
