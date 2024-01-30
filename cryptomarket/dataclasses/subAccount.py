from dataclasses import dataclass
from enum import Enum


class SubAccountStatus(str, Enum):
    NEW = 'new'
    ACTIVE = 'active'
    DISABLE = 'disable'


@dataclass
class SubAccount:
    sub_account_id: str
    email: str
    status: SubAccountStatus
