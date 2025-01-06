from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from cryptomarket.args import ContingencyType, OrderStatus, OrderType, Side, TimeInForce
from cryptomarket.dataclasses.tradeOfOrder import TradeOfOrder


@dataclass
class Order:
    id: int
    client_order_id: str
    symbol: str
    side: Side
    status: OrderStatus
    type: OrderType
    time_in_force: TimeInForce
    quantity: str
    quantity_cumulative: str
    created_at: str
    updated_at: str
    price_average: str
    price: Optional[str] = None
    expire_time: Optional[str] = None
    stop_price: Optional[str] = None
    post_only: Optional[bool] = None
    original_client_order_id: Optional[str] = None
    order_list_id: Optional[str] = None
    contingency_type: Optional[ContingencyType] = None
    trades: Optional[List[TradeOfOrder]] = None
