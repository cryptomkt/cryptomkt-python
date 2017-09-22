# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import warnings

import requests

from exchange.auth import HMACAuth
from exchange.model import APIObject, new_api_object, Order
from exchange.util import check_uri_security, encode_params
from exchange.error import build_api_error


from exchange.compat import imap
from exchange.compat import quote
from exchange.compat import urljoin
from exchange.compat import urlencode


class Client(object):

    BASE_API_URI = 'https://api.cryptomkt.com/'
    API_VERSION = 'v1'

    def __init__(self, api_key, api_secret, base_api_uri=None, api_version=None):
        if not api_key:
            raise ValueError('Missing `api_key`.')
        if not api_secret:
            raise ValueError('Missing `api_secret`.')

            # Allow passing in a different API base.
        self.BASE_API_URI = check_uri_security(base_api_uri or self.BASE_API_URI)

        self.API_VERSION = api_version or self.API_VERSION

        # Set up a requests session for interacting with the API.
        self.session = self._build_session(HMACAuth, api_key, api_secret, self.API_VERSION)

    def _build_session(self, auth_class, *args, **kwargs):
        """Internal helper for creating a requests `session` with the correct
        authentication handling."""
        session = requests.session()
        session.auth = auth_class(*args, **kwargs)
        # session.headers.update({'Content-Type': 'application/json'})
        return session

    def _create_api_uri(self, *parts, **kwargs):
        """Internal helper for creating fully qualified endpoint URIs."""

        params = kwargs.get("params", None)

        if params and isinstance(params, dict):
            url = urljoin(self.BASE_API_URI, '/'.join(imap(quote, parts)) + '?%s' % urlencode(params))
        else:
            url = urljoin(self.BASE_API_URI, '/'.join(imap(quote, parts)))
        return url

    def _request(self, method, *relative_path_parts, **kwargs):
        """Internal helper for creating HTTP requests to the CryptoMarket API.
        Raises an APIError if the response is not 20X. Otherwise, returns the
        response object. Not intended for direct use by API consumers.
        """
        uri = self._create_api_uri(*relative_path_parts, **kwargs)

        data = kwargs.get("data", None)
        if data and isinstance(data, dict):
            kwargs['data'] = data

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the CryptoMarket server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status_code).startswith('2'):
            raise build_api_error(response)
        return response

    def _get(self, *args, **kwargs):
        return self._request('get', *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)

    def _make_api_object(self, response, model_type=None):
        blob = response.json()
        data = blob.get('data', None)
        # All valid responses have a "data" key.
        if data is None:
            raise build_api_error(response, blob)
        # Warn the user about each warning that was returned.
        warnings_data = blob.get('warnings', None)
        for warning_blob in warnings_data or []:
            message = "%s (%s)" % (
                warning_blob.get('message', ''),
                warning_blob.get('url', ''))
            warnings.warn(message, UserWarning)

        pagination = blob.get('pagination', None)
        kwargs = {
            'response': response,
            'pagination': pagination and new_api_object(None, pagination, APIObject),
            'warnings': warnings_data and new_api_object(None, warnings_data, APIObject),
        }

        if isinstance(data, dict):
            obj = new_api_object(self, data, model_type, **kwargs)
        else:
            obj = APIObject(self, **kwargs)
            obj.data = new_api_object(self, data, model_type)
        return obj

    # Public API
    # -----------------------------------------------------------

    def get_markets(self):
        """https://developers.cryptomkt.com/es/#mercado"""
        response = self._get('v1', 'market')
        return self._make_api_object(response, APIObject)

    def get_ticker(self, market=None):
        """https://developers.cryptomkt.com/es/#obtener-ticker"""
        params = {}

        if market:
            params['market'] = market

        response = self._get('v1', 'ticker', params=params)
        return self._make_api_object(response, APIObject)

    def get_book(self, market, type, page=None, limit=None):
        """https://developers.cryptomkt.com/es/#libro-de-ordenes"""
        params = dict(
            market=market,
            type=type
        )

        if page and isinstance(page, int):
            params['page'] = page

        if limit and isinstance(limit, int):
            params['limit'] = limit

        response = self._get('v1', 'book', params=params)
        return self._make_api_object(response, APIObject)

    def get_trades(self, market, start=None, end=None, page=None, limit=None):
        """https://developers.cryptomkt.com/es/#obtener-trades"""
        params = dict(
            market=market
        )

        if start:
            params['start'] = start

        if end:
            params['end'] = end

        if page:
            params['page'] = page

        if limit:
            params['limit'] = limit

        response = self._get('v1', 'trades', params=params)
        return self._make_api_object(response, APIObject)

    def get_active_orders(self, market, page=None, limit=None):
        """https://developers.cryptomkt.com/es/#ordenes-activas"""
        params = dict(
            market=market
        )

        if page:
            params['page'] = page

        if limit:
            params['limit'] = limit

        response = self._get('v1', 'orders', 'active', params=params)
        return self._make_api_object(response, Order)

    def get_executed_orders(self, market, page=None, limit=None):
        """https://developers.cryptomkt.com/es/#ordenes-activas"""
        params = dict(
            market=market
        )

        if page:
            params['page'] = page

        if limit:
            params['limit'] = limit

        response = self._get('v1', 'orders', 'executed', params=params)
        return self._make_api_object(response, Order)

    def create_order(self, market, amount, price, type):
        """https://developers.cryptomkt.com/es/?python#crear-orden"""
        params = dict(
            market=market,
            amount=amount,
            price=price,
            type=type
        )

        response = self._post('v1', 'orders', 'create', data=params)
        return self._make_api_object(response, Order)

    def get_status_order(self, id):
        """https://developers.cryptomkt.com/es/?python#estado-de-orden"""
        params = dict(
            id=id
        )

        response = self._get('v1', 'orders', 'status', params=params)
        return self._make_api_object(response, Order)

    def cancel_order(self, id):
        """https://developers.cryptomkt.com/es/?python#cancelar-una-orden"""
        params = dict(
            id=id
        )

        response = self._post('v1', 'orders', 'cancel', data=params)
        return self._make_api_object(response, Order)

    def get_balance(self):
        """https://developers.cryptomkt.com/es/?python#obtener-balance"""

        response = self._get('v1', 'balance')
        return self._make_api_object(response, APIObject)