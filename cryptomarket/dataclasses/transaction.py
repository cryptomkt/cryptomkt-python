from dataclasses import dataclass
from typing import Any
from cryptomarket.dataclasses.metaTransaction import MetaTransaction

from cryptomarket.dataclasses.nativeTransaction import NativeTransaction


@dataclass
class Transaction:
    id: int = None
    status: str = None
    type: str = None
    subtype: str = None
    created_at: str = None
    updated_at: str = None
    primetrust: Any = None
    native: NativeTransaction = None
    meta: MetaTransaction = None
