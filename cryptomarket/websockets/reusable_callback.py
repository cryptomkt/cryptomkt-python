from dataclasses import dataclass
from typing import Callable, Optional, Tuple


@dataclass
class ReusableCallback:
    callback: Callable
    call_count: int

    def is_done(self) -> bool:
        return self.call_count < 1

    def get_callback(self) -> Optional[Tuple[Callable, bool]]:
        if self.is_done():
            return None, True
        self.call_count -= 1
        return self.callback, self.is_done()
