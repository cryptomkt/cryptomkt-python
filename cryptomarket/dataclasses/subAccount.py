from dataclasses import dataclass
from typing import Literal


@dataclass
class SubAccount:
    sub_account_id: str
    email: str
    status: Literal['new', 'active', 'disable']
