from dataclasses import dataclass
from typing import Optional, Tuple, Generic

from cryptomarket.websockets.callback import T, Callback


@dataclass
class ReusableCallback(Generic[T]):
    callback: Callback[T]
    call_count: int

    def is_done(self) -> bool:
        return self.call_count < 1

    def get_callback(self) -> Tuple[Optional[Callback[T]], bool]:
        if self.is_done():
            return None, True
        self.call_count -= 1
        return self.callback, self.is_done()
