import time

from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.websockets.callback_cache import CallbackCache
from cryptomarket.websockets.manager import WebsocketManager
from typing import Dict


class ClientBase:
    def __init__(
        self, 
        uri:str, 
        subscription_keys:Dict[str,str]={}, 
        on_connect=None, 
        on_error=None, 
        on_close=None
    ):
        self.ws_manager = WebsocketManager(self, uri)    
        self.callback_cache = CallbackCache()
        self.subscription_keys = subscription_keys

        if on_connect is not None: self.on_connect = on_connect
        else: self.on_connect = lambda: None

        if on_error is not None: self.error = on_error
        else: self._on_error = lambda err: None

        if on_close is not None: self.on_close = on_close
        else: self.on_close = lambda: None

    def connect(self):
        """connnects via websocket to the exchange.

        If the websocket requires authentication, it also authenticates and then resolves.
        """
        self.ws_manager.connect()
        while not self.ws_manager.connected:
            time.sleep(1)
    
    def close(self):
        """close the websocket connection with the exchange
        """
        self.ws_manager.close()
        
    def _on_open(self):
        """
        internal use only
        """
        self.on_connect()

    # sends #

    def send_subscription(self, method, callback, params=None, result_callback=None):
        key = self.build_key(method, params)
        self.callback_cache.store_subscription_callback(key, callback)
        self.send_by_id(method, result_callback, params)

    def send_unsubscription(self, method, callback=None, params=None):
        key = self.build_key(method, params)
        self.callback_cache.delete_subscription_callback(key)
        self.send_by_id(method, callback, params)

    def send_by_id(self, method: str, callback: callable=None, params=None):
        payload = {'method':method, 'params':params}
        if callback is not None:
            id = self.callback_cache.store_callback(callback)
            payload['id'] = id
        self.ws_manager.send(payload)
    
    # handles #

    def handle(self, message):
        if 'method' in message:
            self.handle_notification(message)
        elif 'id' in message:
            self.handle_response(message)
    
    def handle_notification(self, message):
        method = message['method']
        if 'params' not in message:
            return
        params = message['params']
        key = self.build_key(method, params)

        callback = self.callback_cache.get_subscription_callback(key)
        if callback is not None:
            if type(message["params"])==list:
                for feed in message["params"]:
                    callback(feed)
            else:
                callback(message["params"])

    def handle_response(self, response):
        id = response['id']
        callback = self.callback_cache.pop_callback(id)
        if callback is None: return

        if 'error' in response:
            callback(CryptomarketAPIException.from_dict(response), None)
        elif 'result' in response:
            result = response['result']
            if type(result)==dict and 'data' in result: 
                callback(None, result['data'])
            else: 
                callback(None, result)

    def build_key(self, method, params):
        if not method in self.subscription_keys: 
            return "subscription"
        return self.subscription_keys[method]
