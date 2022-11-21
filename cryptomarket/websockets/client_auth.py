import time
from typing import Dict
from cryptomarket.exceptions import CryptomarketSDKException

from cryptomarket.hmac import HS256
from cryptomarket.websockets.client_base import ClientBase


class ClientAuth(ClientBase):
    def __init__(
        self,
        uri: str,
        api_key: str,
        api_secret: str,
        window: int = None,
        subscription_methods_data: Dict[str, str] = {},
        on_connect=None,
        on_error=None,
        on_close=None
    ):
        super(ClientAuth, self).__init__(
            uri,
            subscription_methods_data=subscription_methods_data,
            on_connect=on_connect,
            on_error=on_error,
            on_close=on_close
        )
        self.window = window
        self.api_key = api_key
        self.api_secret = api_secret
        self.authed = False

    def connect(self):
        super().connect()

        def wait_auth(err, result):
            if err is not None:
                raise err
            self.authed = True
        self.authenticate(wait_auth)
        n_tries = 10
        try_number = 1
        while not self.authed and try_number < n_tries:
            try_number += 1
            time.sleep(1)
        if not self.authed:
            raise CryptomarketSDKException('Authentication failed')

    def authenticate(self, callback: callable = None):
        """Authenticates the websocket

        https://api.exchange.cryptomkt.com/#socket-session-authentication

        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The transaction status as result argument for the callback.

        .. code-block:: python
        True
        """
        timestamp = int(time.time())
        msg = [str(timestamp)]
        if self.window:
            msg.append(str(self.window*1000))
        signature = HS256.get_signature(''.join(msg), self.api_secret)
        params = {
            'type': 'HS256',
            'api_key': self.api_key,
            'timestamp': timestamp,
            'signature': signature,
        }
        if self.window:
            params['window'] = self.window
        return self._send_by_id(method='login', callback=callback, params=params)
