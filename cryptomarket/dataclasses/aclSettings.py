from dataclasses import dataclass


@dataclass
class ACLSettings:
    sub_account_id: str = None
    deposit_address_generation_enabled: bool = None
    withdraw_enabled: bool = None
    description: str = None
    created_at: str = None
    updated_at: str = None
