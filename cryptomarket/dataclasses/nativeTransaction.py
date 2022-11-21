from dataclasses import dataclass, field
from typing import List


@dataclass
class NativeTransaction:
    tx_id: str = None
    index: int = None
    currency: str = None
    amount: str = None
    fee: str = None
    address: str = None
    payment_id: str = None
    hash: str = None
    offchain_id: str = None
    confirmations: int = None
    public_comment: str = None
    error_code: str = None
    senders: List[str] = field(default_factory=list)
