# coding=utf-8

import requests

from cryptomarket.exceptions import CryptomarketAPIException
from cryptomarket.hmac import HS256

api_url = 'https://api.exchange.cryptomkt.com/api/2/'

class HttpClient:

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.session_is_open = False
        self.session = None
        self._init_session()
    
    def _init_session(self):
        assert self.session_is_open == False
        session = requests.session()
        session.headers.update({'User-Agent': 'cryptomarket/python'})
        self.session = session
        self.session_is_open = True

    def close_session(self):
        self.session.close()
        self.session_is_open = False
    
    def authorize(self):
        assert self.session_is_open == True
        self.session.auth = HS256(self.api_key, self.secret_key)

    def get(self, endpoint, params=None):
        response = self.session.get(api_url + endpoint, params=params)
        return self._handle_response(response)

    def post(self, endpoint, params=None):
        response = self.session.post(api_url + endpoint, data=params)
        return self._handle_response(response)

    def put(self, endpoint, params=None):
        response = self.session.put(api_url + endpoint, params=params)
        return self._handle_response(response)

    def delete(self, endpoint, params=None):
        response = self.session.delete(api_url + endpoint, params=params)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the CryptoMarket server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status_code).startswith('2'):
            raise CryptomarketAPIException(response)
        try:
            return response.json()
        except ValueError:
            raise Exception(f'Invalid Response: {response}')
