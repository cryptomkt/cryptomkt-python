from dataclasses import dataclass
from typing import Mapping, Optional


@dataclass
class Network:
    network: str
    default: bool
    payin_enabled: bool
    payout_enabled: bool
    precision_payout: str
    payout_is_payment_id: bool
    payin_payment_id: bool
    payin_confirmations: int
    protocol: Optional[str] = None
    payout_fee: Optional[str] = None
    address_regrex: Optional[str] = None
    payment_id_regex: Optional[str] = None
    low_processing_time: Optional[str] = None
    high_processing_time: Optional[str] = None
    avg_processing_time: Optional[str] = None
    crypto_payment_id_name: Optional[str] = None
    crypto_explorer: Optional[str] = None
    code: Optional[str] = None
    is_ens_available: Optional[bool] = None
    network_name: Optional[str] = None
    contract_address: Optional[str] = None
    is_multichain: Optional[bool] = None
    asset_id: Optional[Mapping[str,str]] = None
