from dataclasses import dataclass
from typing import Literal


@dataclass
class SubscriptionMethodData:
    subscription: str
    method_type: Literal['snapshot', 'update', 'data', 'command']
