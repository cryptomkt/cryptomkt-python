from typing import Any, Callable, Dict, Optional
from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.websockets.callback import Callback
from cryptomarket.websockets.reusable_callback import ReusableCallback
from dacite.data import Data


class CallbackCache:
    def __init__(self):
        self.callbacks: Dict[int, ReusableCallback] = {}
        self.subscription_callbacks: Dict[int, Callback[Any]] = {}
        self._id = 1

    def next_id(self):
        self._id += 1
        if self._id < 1:
            self._id = 1
        return self._id

    def save_callback(self, callback: Callback[Any], call_count: int = 1) -> int:
        id = self.next_id()
        self.callbacks[id] = ReusableCallback(callback, call_count)
        return id

    def get_callback(self, id: int) -> Optional[Callback[Any]]:
        if id not in self.callbacks:
            return None
        reusable_callback = self.callbacks[id]
        callback, done = reusable_callback.get_callback()
        if done:
            del self.callbacks[id]
        return callback

    def save_subscription_callback(self, key: int, callback: Callback[Any]):
        self.subscription_callbacks[key] = callback

    def get_subscription_callback(self, key: int) -> Optional[Callback[Any]]:
        if key not in self.subscription_callbacks:
            return None
        return self.subscription_callbacks[key]

    def delete_subscription_callback(self, key: str):
        if key in self.callbacks:
            del self.callbacks[key]
