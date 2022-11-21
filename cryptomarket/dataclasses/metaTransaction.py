from dataclasses import dataclass


@dataclass
class MetaTransaction:
    fiat_to_crypto: str
    id: int
    provider_name: str
    order_type: str
    order_type: str
    source_currency: str
    target_currency: str
    wallet_address: str
    tx_hash: str
    target_amount: str
    source_amount: str
    status: str
    created_at: str
    updated_at: str
    deleted_at: str
    payment_method_type: str
