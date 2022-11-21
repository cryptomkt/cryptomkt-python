from dataclasses import dataclass


@dataclass
class Address:
    address: str = None
    currency: str = None
    payment_id: str = None
    public_key: str = None
