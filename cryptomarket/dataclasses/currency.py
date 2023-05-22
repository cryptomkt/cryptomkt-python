from dataclasses import dataclass
from typing import List, Optional

from cryptomarket.dataclasses.network import Network


@dataclass
class Currency:
    full_name: str
    crypto: bool
    payin_enabled: bool
    payout_enabled: bool
    transfer_enabled: bool
    sign: str
    crypto_payment_id_name: str
    crypto_explorer: str
    precision_transfer: str
    delisted: bool
    account_top_order: Optional[int] = None
    qr_prefix: Optional[str] = None
    networks: Optional[List[Network]] = None
