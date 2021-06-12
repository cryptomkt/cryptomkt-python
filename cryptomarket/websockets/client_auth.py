import random
import string
import time
from typing import Any, Dict, List, Union

from cryptomarket.hmac import HS256
from cryptomarket.websockets.client_base import ClientBase


class ClientAuth(ClientBase):
    def __init__(
        self, 
        uri:str, 
        api_key:str, 
        api_secret:str, 
        subscription_keys:Dict[str, str]={}, 
        on_connect=None, 
        on_error=None, 
        on_close=None
    ):
        super(ClientAuth, self).__init__(
            uri, 
            subscription_keys=subscription_keys, 
            on_connect=on_connect, 
            on_error=on_error, 
            on_close=on_close
        )
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
        while not self.authed:
            time.sleep(1)
        
    
    def authenticate(self, callback: callable=None):
        """Authenticates the websocket

        https://api.exchange.cryptomkt.com/#socket-session-authentication

        :param callback: Optional. A callable to call with the result data. It takes two arguments, err and result. err is None for successful calls, result is None for calls with error: callback(err, result).

        :returns: The transaction status as result argument for the callback.

        .. code-block:: python
        True
        """
        letters = string.ascii_letters
        nonce = ''.join(random.choice(letters) for i in range(30))  
        signature = HS256.get_signature(nonce, self.api_secret)
        params = {
            'algo': 'HS256',
            'pKey': self.api_key,
            'nonce': nonce,
            'signature': signature,
        }
        return self.send_by_id(method='login', callback=callback, params=params)
