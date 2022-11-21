import time

from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.websockets.callback_cache import CallbackCache
from cryptomarket.websockets.manager import WebsocketManager
from typing import Dict

from cryptomarket.websockets.subscriptionMethodData import SubscriptionMethodData


class ClientBase:
    def __init__(
        self,
        uri: str,
        subscription_methods_data: Dict[str, SubscriptionMethodData] = {},
        on_connect=None,
        on_error=None,
        on_close=None
    ):
        if on_connect is not None:
            self.on_connect = on_connect
        else:
            self.on_connect = lambda: None

        if on_error is not None:
            self.error = on_error
        else:
            self._on_error = lambda err: None

        if on_close is not None:
            self.on_close = on_close
        else:
            self.on_close = lambda: None
        self._ws_manager = WebsocketManager(self, uri)
        self._callback_cache = CallbackCache()
        self._subscription_methods_data = subscription_methods_data

    def connect(self):
        """connnects via websocket to the exchange.

        If the websocket requires authentication, it also authenticates and then resolves.
        """
        self._ws_manager.connect()
        while not self._ws_manager.connected:
            time.sleep(1)

    def close(self):
        """close the websocket connection with the exchange
        """
        self._ws_manager.close()

    def _on_open(self):
        """
        internal use only
        """
        self.on_connect()

    # sends #

    def _send_subscription(self, method, callback, params=None, result_callback=None):
        key = self._build_key(method)
        self._callback_cache.store_subscription_callback(key, callback)
        self._send_by_id(method, result_callback, params)

    def _send_unsubscription(self, method, callback=None, params=None):
        key = self._build_key(method)
        self._callback_cache.delete_subscription_callback(key)
        self._send_by_id(method, callback, params)

    def _send_by_id(self, method: str, callback: callable = None, params=None):
        payload = {'method': method, 'params': params}
        if callback is not None:
            id = self._callback_cache.store_callback(callback)
            payload['id'] = id
        self._ws_manager.send(payload)

    # handles #

    def _handle(self, message):
        if 'method' in message:
            self._handle_notification(message)
        elif 'id' in message:
            self._handle_response(message)

    def _handle_notification(self, message):
        method = message['method']
        if 'params' not in message:
            return
        params = message['params']
        key = self._build_key(method)
        method_type = 'update'
        if key != 'subscription':
          method_type = self._subscription_methods_data[method].method_type
        callback = self._callback_cache.get_subscription_callback(key)
        callback(params, method_type)

    def _handle_response(self, response):
        id = response['id']
        callback = self._callback_cache.pop_callback(id)
        if callback is None:
            return

        if 'error' in response:
            callback(CryptomarketAPIException.from_dict(response), None)
        elif 'result' in response:
            result = response['result']
            if type(result) == dict and 'data' in result:
                callback(None, result['data'])
            else:
                callback(None, result)

    def _build_key(self, method):
        if not method in self._subscription_methods_data:
            return "subscription"
        return self._subscription_methods_data[method].subscription
