import time
from datetime import datetime, timedelta
from typing import Dict, Optional

from cryptomarket.exceptions import (CryptomarketAPIException,
                                     CryptomarketSDKException)
from cryptomarket.websockets.callback_cache import CallbackCache
from cryptomarket.websockets.manager import WebsocketManager
from cryptomarket.websockets.subscriptionMethodData import \
    SubscriptionMethodData


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

    def connect(self, timeout=30) -> Optional[CryptomarketSDKException]:
        """connnects via websocket to the exchange.

        If the websocket requires authentication, it also authenticates and then resolves.

        :param timeout: Seconds the the client will have to connect and then authenticate (if is an authenticated client).
        """
        self._ws_manager.connect()

        timeout_time = datetime.now()+timedelta(seconds=timeout)

        def connecting():
            return not self._ws_manager.connected and datetime.now() < timeout_time
        while connecting():
            time.sleep(1)
        if not self._ws_manager.connected:
            self.close()
            return CryptomarketSDKException("connection timeout")

    def close(self):
        """close the websocket connection with the exchange
        """
        self._ws_manager.close()

    def _on_open(self):
        """
        internal use only
        """
        self.on_connect()

    # SENDS #

    def _send_subscription(self, method, callback, params=None, result_callback=None):
        key = self._build_key(method)
        self._callback_cache.save_subscription_callback(key, callback)
        self._send_by_id(method, result_callback, params)

    def _send_unsubscription(self, method, callback=None, params=None):
        key = self._build_key(method)
        self._callback_cache.delete_subscription_callback(key)
        self._send_by_id(method, callback, params)

    def _send_by_id(self, method: str, callback: callable = None, params=None, call_count: int = 1):
        payload = {'method': method, 'params': params}
        if callback:
            id = self._callback_cache.save_callback(callback, call_count)
            payload['id'] = id
        self._ws_manager.send(payload)

    # HANDLES #

    def _handle(self, message):
        if 'id' in message:
            self._handle_response(message)
        elif 'method' in message:
            self._handle_notification(message)

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
        callback = self._callback_cache.get_callback(id)
        if callback is None:
            return
        if 'error' in response:
            callback(CryptomarketAPIException.from_dict(response), None)
            return
        if 'result' in response:
            result = response['result']
            if type(result) == dict and 'data' in result:
                callback(None, result['data'])
            else:
                callback(None, result)

    def _build_key(self, method):
        if not method in self._subscription_methods_data:
            return "subscription"
        return self._subscription_methods_data[method].subscription
