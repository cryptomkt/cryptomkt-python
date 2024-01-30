from dataclasses import dataclass

from typing_extensions import Literal


@dataclass
class SubscriptionMethodData:
    subscription: str
    method_type: Literal['snapshot', 'update', 'data', 'command']
