from dataclasses import dataclass


@dataclass
class Report:
    id: int = None
    client_order_id: str = None
    symbol: str = None
    side: str = None
    status: str = None
    type: str = None
    time_in_force: str = None
    quantity: str = None
    price: str = None
    cum_quantity: str = None
    post_only: bool = None
    created_at: str = None
    updated_at: str = None
    stop_price: str = None
    expire_time: str = None
    original_client_order_id: str = None
    trade_id: str = None
    trade_quantity: str = None
    trade_price: str = None
    trade_fee: str = None
    trade_taker: bool = None
    report_type: str = None
    order_list_id: str = None
    contingency_type: str = None
