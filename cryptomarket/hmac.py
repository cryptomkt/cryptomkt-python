import hashlib
import hmac
import time
from base64 import b64encode
from urllib.parse import urlparse

from requests.auth import AuthBase


class HS256(AuthBase):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, r):
        url = urlparse(r.url)
        timestamp = str(int(time.time()))
        msg = r.method + timestamp + url.path
        if url.query != "":
            msg += "?" + url.query
        if r.body:
            msg += r.body

        signature = hmac.new(self.password.encode(), msg.encode(), hashlib.sha256).hexdigest()
        authstr = "HS256 " + b64encode(
                    b':'.join((self.username.encode(), timestamp.encode(), signature.encode()))).decode().strip()
        r.headers['Authorization'] = authstr
        return r

    @staticmethod
    def get_signature(message, password):
        return hmac.new(password.encode(), message.encode(), hashlib.sha256).hexdigest()

