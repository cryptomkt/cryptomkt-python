# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import hashlib
import hmac
import json
import time

from requests.auth import AuthBase
from requests.utils import to_native_string

#same folder
from .compat import urljoin, urlparse


class HMACAuth(AuthBase):
    def __init__(self, api_key, api_secret, api_version):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_version = api_version

    def __call__(self, request):

        body = ''

        if request.body:
            params = dict(map(lambda x: x.split('='), request.body.split('&')))
            keys = list(params)
            keys.sort()
            for key in keys:
                body += str(params[key])

        timestamp = str(int(time.time()))
        message = timestamp + urljoin(request.path_url, urlparse(request.path_url).path) + body
        secret = self.api_secret

        if not isinstance(message, bytes):
            message = message.encode()
        if not isinstance(secret, bytes):
            secret = secret.encode()
        signature = hmac.new(secret, message, hashlib.sha384).hexdigest()

        request.headers.update({
            to_native_string('X-MKT-APIKEY'): self.api_key,
            to_native_string('X-MKT-SIGNATURE'): signature,
            to_native_string('X-MKT-TIMESTAMP'): timestamp,
        })

        return request
