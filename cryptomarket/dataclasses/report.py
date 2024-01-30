from dataclasses import dataclass
from enum import Enum
from typing import Optional

from cryptomarket.args import ContingencyType, OrderType, Side, TimeInForce
from cryptomarket.dataclasses.order import OrderStatus


class ReportType(str, Enum):
    STATUS = 'status'
    NEW = 'new'
    SUSPENDED = 'suspended'
    CANCELED = 'canceled'
    REJECTED = 'rejected'
    EXPIRED = 'expired'
    REPLACED = 'replaced'
    TRADE = 'trade'


@dataclass
class Report:
    id: int
    client_order_id: str
    symbol: str
    side: Side
    status: OrderStatus
    type: OrderType
    time_in_force: TimeInForce
    quantity: str
    quantity_cumulative: str
    post_only: bool
    created_at: str
    updated_at: str
    report_type: Optional[ReportType] = None
    price: Optional[str] = None
    stop_price: Optional[str] = None
    expire_time: Optional[str] = None
    original_client_order_id: Optional[str] = None
    trade_id: Optional[str] = None
    trade_quantity: Optional[str] = None
    trade_price: Optional[str] = None
    trade_fee: Optional[str] = None
    trade_taker: Optional[bool] = None
    order_list_id: Optional[str] = None
    contingency_type: Optional[ContingencyType] = None
