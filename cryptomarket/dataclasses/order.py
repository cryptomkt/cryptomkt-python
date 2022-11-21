from dataclasses import dataclass, field
from typing import List, Literal, Union

from cryptomarket.dataclasses.tradeOfOrder import TradeOfOrder


@dataclass
class Order:
    id: int = None
    client_order_id: str = None
    symbol: str = None
    side: Literal['buy', 'sell'] = None
    status: Literal[
        'new', 'suspended', 'takeProfitMarket', 'partiallyFilled', 'filled', 'canceled', 'expired'
    ] = None
    type: Literal[
        'limit', 'market', 'stopLimit', 'stopMarket', 'takeProfitLimit', 'takeProfitMarket'
    ] = None
    time_in_force: Literal['GTC', 'IOC', 'FOK', 'GTD'] = None
    quantity: str = None
    price: str = None
    quantity_cumulative: str = None
    created_at: str = None
    updated_at: str = None
    expire_time: str = None
    stop_price: str = None
    post_only: bool = None
    trades: List[TradeOfOrder] = field(default_factory=list)
    original_client_order_id: str = None
    order_list_id: str = None
    contingency_type: Union[Literal[
        'allOrNone', 'oneCancelOther', 'oneTriggerOneCancelOther'
    ], None] = None
