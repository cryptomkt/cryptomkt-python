from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ErrorCode(str, Enum):
    INVALID_ADDRESS = 'INVALID_ADDRESS'
    INVALID_PAYMENT_ID = 'INVALID_PAYMENT_ID'
    BAD_PRECISION = 'BAD_PRECISION'


@dataclass
class NativeTransaction:
    tx_id: str
    index: int
    currency: str
    amount: str
    fee: Optional[str] = None
    address: Optional[str] = None
    payment_id: Optional[str] = None
    hash: Optional[str] = None
    offchain_id: Optional[str] = None
    confirmations: Optional[int] = None
    public_comment: Optional[str] = None
    error_code: Optional[ErrorCode] = None
    senders: Optional[List[str]] = None
