from typing import Callable, Generic, Optional, TypeVar
from dacite.data import Data

from cryptomarket.exceptions import CryptomarketAPIException

T = TypeVar('T')
Callback = Callable[[Optional[CryptomarketAPIException], Optional[T]], None]