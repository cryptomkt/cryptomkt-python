from dataclasses import dataclass
from typing import Optional


@dataclass
class ACLSettings:
    sub_account_id: str
    deposit_address_generation_enabled: bool
    withdraw_enabled: bool
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
