from typing import Callable, Dict, Optional
from cryptomarket.websockets.reusable_callback import ReusableCallback


class CallbackCache:
    def __init__(self):
        self.callbacks: Dict[str, ReusableCallback] = dict()
        self._id = 1

    def next_id(self):
        self._id += 1
        if self._id < 1:
            self._id = 1
        return self._id

    def save_callback(self, callback: callable, call_count: int = 1) -> int:
        id = self.next_id()
        self.callbacks[id] = ReusableCallback(callback, call_count)
        return id

    def get_callback(self, id: int) -> Optional[Callable]:
        if id not in self.callbacks:
            return None
        reusable_callback = self.callbacks[id]
        callback, done = reusable_callback.get_callback()
        if done:
            del self.callbacks[id]
        return callback

    def save_subscription_callback(self, key: str, callback: callable):
        self.callbacks[key] = callback

    def get_subscription_callback(self, key: str) -> callable:
        if key not in self.callbacks:
            return None
        return self.callbacks[key]

    def delete_subscription_callback(self, key: str):
        if key in self.callbacks:
            del self.callbacks[key]
