from dataclasses import dataclass
from typing import Optional

from cryptomarket.args import (TransactionStatus, TransactionSubType,
                               TransactionType)
from cryptomarket.dataclasses.metaTransaction import MetaTransaction
from cryptomarket.dataclasses.nativeTransaction import NativeTransaction


@dataclass
class Transaction:
    id: int
    status: TransactionStatus
    type: TransactionType
    subtype: TransactionSubType
    created_at: str
    updated_at: str
    native: Optional[NativeTransaction] = None
    meta: Optional[MetaTransaction] = None
