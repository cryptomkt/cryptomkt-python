class CallbackCache:
    def __init__(self):
        self.callbacks = dict()
        self._id = 1
    
    def next_id(self):
        self._id += 1
        if self._id < 1:
            self._id = 1
        return self._id

    def store_callback(self, callback: callable) -> int:
        id = self.next_id()
        self.callbacks[id] = callback
        return id

    def pop_callback(self, id: int) -> callable:
        if id not in self.callbacks: return None
        callback = self.callbacks[id]
        del self.callbacks[id]
        return callback

    def store_subscription_callback(self, key: str, callback: callable):
        self.callbacks[key] = callback

    def get_subscription_callback(self, key: str) -> callable:
        if key not in self.callbacks: return None
        return self.callbacks[key]

    def delete_subscription_callback(self, key: str):
        if key in self.callbacks: del self.callbacks[key]
        

