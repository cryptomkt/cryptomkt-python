from dataclasses import dataclass, field
from typing import Any, List

from cryptomarket.dataclasses.network import Network


@dataclass
class Currency:
    full_name: str = None
    crypto: bool = None
    payin_enabled: bool = None
    payout_enabled: bool = None
    transfer_enabled: bool = None
    precision_transfer: str = None
    networks: List[Network] = field(default_factory=list)
