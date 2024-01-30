import time
from datetime import datetime, timedelta
from typing import Dict, Optional

from cryptomarket.exceptions import (CryptomarketAPIException,
                                     CryptomarketSDKException)
from cryptomarket.hmac_auth import HmacAuth
from cryptomarket.websockets.client_base import ClientBase


class ClientAuthenticable(ClientBase):
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
        super(ClientAuthenticable, self).__init__(
            uri,
            subscription_methods_data=subscription_methods_data,
            on_connect=on_connect,
            on_error=on_error,
            on_close=on_close
        )
        self.window = window
        self.api_key = api_key
        self.api_secret = api_secret
        self.authed: bool = False
        self._auth_error: Optional[CryptomarketAPIException] = None

    def connect(self, timeout=30) -> Optional[CryptomarketSDKException]:
        timeout_time = datetime.now()+timedelta(seconds=timeout)
        err = super().connect(timeout)
        if err:
            return err

        def authenticate_client(err, result):
            if err:
                self._auth_error = err
            elif result:
                self.authed = True
            else:
                self._auth_error = CryptomarketSDKException(
                    'authentication failed')
        self.authenticate(authenticate_client)

        def auth_done():
            return self.authed or self._auth_error or datetime.now() >= timeout_time
        while not auth_done():
            time.sleep(1)

        if self._auth_error:
            self.close()
            return self._auth_error
        if not self.authed:
            self.close()
            return CryptomarketSDKException('authentication timeout')

    def authenticate(self, callback: callable = None):
        """Authenticates the websocket

        https://api.exchange.cryptomkt.com/#socket-session-authentication

        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The transaction status as result argument for the callback.

        .. code-block:: python
        True
        """
        timestamp = int(time.time()*1_000)
        msg = str(timestamp)
        if self.window:
            msg += str(self.window)
        signature = HmacAuth.get_signature(msg, self.api_secret)
        params = {
            'type': 'HS256',
            'api_key': self.api_key,
            'timestamp': timestamp,
            'signature': signature,
        }
        if self.window:
            params['window'] = self.window
        return self._send_by_id(method='login', callback=callback, params=params)
