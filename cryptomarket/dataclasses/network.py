from dataclasses import dataclass


@dataclass
class Network:
    network: str = None
    protocol: str = None
    default: bool = None
    payin_enabled: bool = None
    payout_enabled: bool = None
    precision_payout: str = None
    payout_fee: str = None
    payout_is_payment_id: bool = None
    payin_payment_id: bool = None
    payin_confirmations: int = None
    address_regrex: str = None
    payment_id_regex: str = None
    low_processing_time: str = None
    high_processing_time: str = None
    avg_processing_time: str = None
