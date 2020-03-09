# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import warnings
import time

import requests

from .auth import HMACAuth
from .model import APIObject, new_api_object, Order
from .util import check_uri_security, encode_params
from .error import build_api_error  


from .compat import imap
from .compat import quote
from .compat import urljoin
from .compat import urlencode


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

        # a container for the socket if needed.
        self.socket = None

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
        """Returns a list of the marketpairs as strings available in Cryptomkt
        as the "data" member of a dict.
        
        Does not requiere to be authenticated.

        https://developers.cryptomkt.com/#mercado
        """
        response = self._get(self.API_VERSION, 'market')
        return self._make_api_object(response, APIObject)


    def get_ticker(self, market=None):
        """Returns a general view of the market state as a dict.
        shows the actual bid and ask, also the volume and price, 
        and the low and high.

        Does not requiere to be authenticated.

        Arguments:
            market: A market pair as string, if no market pair is provided, 
                the market state of all the market pairs are returned.
                e.g: 'EHTARS'.

        https://developers.cryptomkt.com/#obtener-ticker
        """
        params = {}

        if market:
            params['market'] = market

        response = self._get(self.API_VERSION, 'ticker', params=params)
        return self._make_api_object(response, APIObject)


    def get_book(self, market, type_, page=None, limit=None):
        """Returns a list of active orders of a given type in a specified
        market pair.

        Does not requiere to be authenticated.

        Required Arguments:
            market: A market pair as a string. Is the specified market to get
                the book from.
                e.g: 'ETHEUR'.
            type: 'buy' or 'sell'.
        Optional Arguments:
            page: Page number to query. Default is 0
            limit: Number of orders returned in each page. Default is 20.

        https://developers.cryptomkt.com/#libro-de-ordenes
        """
        params = dict(
            market=market,
            type=type_
        )

        if page is not None and isinstance(page, int):
            params['page'] = page

        if limit is not None and isinstance(limit, int):
            params['limit'] = limit

        response = self._get(self.API_VERSION, 'book', params=params)
        return self._make_api_object(response, APIObject)


    def get_trades(self, market, start=None, end=None, page=None, limit=None):
        """returns a list of all trades (executed orders) of a market between 
        the start date, until the end date. the earlier trades first, and the 
        older last.
        If no start date is given, returns trades since 2020-02-17.
        If no end date is given, returns trades until the present moment.

        Does not requiere to be authenticated.
        
        Required Arguments:
            market: A market pair as a string. Is the specified market to get
                the book from.
                e.g: 'ETHCLP'.
        Optional Arguments:
            start: The older date to get trades from, inclusive.
            end: The earlier date to get trades from, exclusive.
            page: Page number to query. Default is 0
            limit: Number of orders returned in each page. Default is 20.


        https://developers.cryptomkt.com/#obtener-trades
        """
        params = dict(
            market=market
        )

        if start is not None:
            params['start'] = start

        if end is not None:
            params['end'] = end

        if page is not None:
            params['page'] = page

        if limit is not None:
            params['limit'] = limit

        response = self._get(self.API_VERSION, 'trades', params=params)
        return self._make_api_object(response, APIObject)


    def get_prices(self, market, timeframe, page = None, limit = None):
        """get_prices(market, timeframe, **kwargs) -> APIObject
        
        This method returns the displayed data in the Market section in CryptoMarket

        You can access the data this way too:
        client.get_prices(args...)["ask or bid (choose one)"][indexYouWant]

        List of arguments:
                Required: market (string), timeframe (string)
                Optional: page (int), limit (int)

        https://developers.cryptomkt.com/#precios
        """
        params = dict(
            market = market,
            timeframe = timeframe
        )
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        response = self._get(self.API_VERSION,"prices", params = params)
        return self._make_api_object(response, APIObject)

    # Authenticated API
    #-------------------------------------------------------------------
    # account 
    def get_account(self):
        """get_account() -> APIObject

        This method displays your account info.

        You can access the info this way:
        client.get_account()["fieldYouWant"]

        This method does not require any arguments

        https://developers.cryptomkt.com/#informacion-de-cuenta
        """
        response = self._get(self.API_VERSION,"account")
        return self._make_api_object(response,APIObject)

    # orders
    def get_active_orders(self, market, page=None, limit=None):
        """get_active_orders(market, **kwargs) -> Order

        This method returns the active order lists in CryptoMarket that belong to
        the owner provided in the client.

        List of arguments:
                Required: market (string)
                Optional: page (int), limit (int)

        https://developers.cryptomkt.com/#ordenes-activas
        """
        params = dict(
            market=market
        )

        if page is not None:
            params['page'] = page

        if limit is not None:
            params['limit'] = limit

        response = self._get(self.API_VERSION, 'orders', 'active', params=params)
        return self._make_api_object(response, Order)

    def get_executed_orders(self, market, page=None, limit=None):
        """get_executed_orders(market,**kwargs) -> Order
        
        This method returns an executed order list in CryptoMarket that belongs to
        the owner provided in the client.

        List of arguments: 
                Required: market (string)
                Optional: page (int), limit (int)

        https://developers.cryptomkt.com/#ordenes-activas
        """
        params = dict(
            market=market
        )

        if page is not None:
            params['page'] = page

        if limit is not None:
            params['limit'] = limit

        response = self._get(self.API_VERSION, 'orders', 'executed', params=params)
        return self._make_api_object(response, Order)

    def create_order(self, market, amount, price, type_):
        """create_order(market, amount, price, type_) -> Order
        
        This method lets you create an sell or buy order inside CryptoMarket. 

        You can access the data this way too:
        client.create_order(args...)["fieldYouWant"]

        List of arguments:
                Required: market (string), amount (string), price (string), type (string)
                This method does not accept any optional args.
        
        https://developers.cryptomkt.com/?python#crear-orden
        """
        params = dict(
            market=market,
            amount=amount,
            price=price,
            type=type_
        )

        response = self._post(self.API_VERSION, 'orders', 'create', data=params)
        return self._make_api_object(response, Order)

    def get_status_order(self, id):
        """get_status_order(id_) -> Order
        
        This method returns the order state of the provided id.
 
        List of arguments:
                Required: id_ (string)
                This method does not accept any optional args.

        https://developers.cryptomkt.com/?python#estado-de-orden
        """
        params = dict(
            id_=id
        )

        response = self._get(self.API_VERSION, 'orders', 'status', params=params)
        return self._make_api_object(response, Order)

    def cancel_order(self, id):
        """cancel_order(id_) -> Order
        
        This method cancels an order.

        You can access the data given this way:
        order.cancel_order()["fieldYouWant"]

        List of arguments:
                Required: id_ (string)
                This method does not accept any optional args.

        https://developers.cryptomkt.com/?python#cancelar-una-orden
        """
        params = dict(
            id_=id
        )

        response = self._post(self.API_VERSION, 'orders', 'cancel', data=params)
        return self._make_api_object(response, Order)
    
    def get_instant(self,market,type_, amount):
        """get_instant(market,type_,amount) -> Order
        
        This method returns, according to the actual market state, the amount in local
        currency or cryptocurrency if a buy or sell is executed.

        You can access the data this way too:
        order.get_instant(args...)["fieldYouWant"]

        List of arguments:
                required: market (string), type_ (string), amount (string)
                This method does not accept any optional args. 

        https://developers.cryptomkt.com/#obtener-cantidad
        """

        rest = float(amount)
        book_type = 'sell' if type_ == 'buy' else 'buy'
        amount_required = 0.0
        amount_obtained = 0.0
        page = 0
        n_entries = 100
        while True:
            book_page = self.get_book(market, book_type, page=page, limit=n_entries)
            for entry in book_page['data']:
                price = float(entry['price'])
                amount = float(entry['amount'])
                if rest < amount:
                    amount_obtained += rest * price
                    amount_required += rest
                    rest = 0
                    break
                else:
                    amount_obtained += amount * price
                    amount_required += amount
                    rest -= amount
            if rest == 0 or len(book_page['data']) < n_entries:
                break
            else: time.sleep(3)
            
            page = page + 1
        
        if book_type == 'sell':
            temp = amount_required
            amount_required = amount_obtained
            amount_obtained = temp
        instant = dict(obtained=amount_obtained, required=amount_required)
        return instant
    
    def create_instant(self,market,type_,amount):
        """create_instant(market, type_, amount) -> Order

        This method creates a instant sell or buy order inside CryptoMarket Instant Exchange.

        List of arguments:
                Required: market (string), type_ (string), amount (string)
                This method doen tno accept any optional args.
        
        https://developers.cryptomkt.com/#crear-orden-2
        """
        params = dict(
            market=market,
            type = type_,
            amount = amount
        )
        response = self._post(self.API_VERSION,"order", "instant", "create", data = params)
        return self._make_api_object(response,Order)
    
    #Wallet
    def get_balance(self):
        """get_balance() -> APIObject

        This method returns your actual wallets balances
        
        You can access the data this way too:
        client.get_balance()[indexYouWant]["fieldYouWant"]

        This method does not require any args.

        https://developers.cryptomkt.com/?python#obtener-balance
        """

        response = self._get(self.API_VERSION, 'balance')
        return self._make_api_object(response, APIObject)
    
    def get_transactions(self, currency, page = None, limit = None):
        """get_transactions(currency, **kwargs) -> APIObject

        This method returns your actual wallets transactions. 

        You can access the data this way too:
        client.get_transactions(args...)[indexYouWant]["fieldYouWant"]

        List of arguments:
                Required: currency (string)
                Optional: page (int), limit (int)

        https://developers.cryptomkt.com/#obtener-movimientos
        """
        params = dict(
            currency = currency
        )

        if page is not None:
            params["page"] = page

        if limit is not None:
            params["limit"] = limit
        
        response = self._get(self.API_VERSION, "transactions", params=params)
        return self._make_api_object(response, APIObject)

    def notify_deposit(self,amount,bank_account, date= None, tracking_code = None, voucher = None):
        """notify_deposit(amount, bank_account, **kwargs) -> APIObject
        
        This method notifies a deposit to a local wallet currency.

        List of arguments:
                Required: amount (string), bank_account (string)
                Required for México: date (string dd/mm/yyyy), tracking_code (string), voucher (file)
                Required for Brazil and European Union: voucher (file)

        https://developers.cryptomkt.com/#notificar-deposito
        """
        params = dict(
            amount = amount,
            bank_account = bank_account            
        )
        if date is not None:
            params["date"] = date 
        if tracking_code is not None:
            params["tracking_code"] = tracking_code
        if voucher is not None:
            params["voucher"] = voucher
        
        response = self._post(self.API_VERSION,"request", "deposit", data = params)
        return self._make_api_object(response,APIObject)

    def notify_withdrawal(self, amount, bank_account):
        """notify_withdrawal(amount, bank_account) -> APIObject
        
        This method notifies a withdrawal froma local currency wallet

        List of arguments:
                Required: amount (string), bank_account (string)
                This method does not accept any optional args.

        https://developers.cryptomkt.com/#notificar-retiro
        """
        params = dict(
            amount = amount,
            bank_account = bank_account
        )
        response = self._post(self.API_VERSION, "request", "withdrawal", data = params)
        return self._make_api_object(response, APIObject)

    def transfer(self,address, amount, currecy, memo = None):
        """transfer(addres, amount, currency, **kwargs) -> APIObject
        
        This method tranfers cryptocurrencies to another wallet

        List of arguments:
                Required: address (string), amount (string), currency (string)
                Optional: memo (string)

        https://developers.cryptomkt.com/#transferir
        """
        params = dict(
            address = address,
            amount = amount,
            currency = currency
        )
        if memo is not None:
            params["memo"] = memo
        
        response = self._post(self.API_VERSION, "transfer", data = params)
        return self._make_api_object(response, APIObject)

    def get_auth_socket(self):
        """get_auth_socket() -> APIObject

        This method returns the data for connecting to websockets, your uid and socid

        This method does not accept any args. 
        """
        response = self._get("v2", "socket/auth")
        return self._make_api_object(response, APIObject)

    def get_socket(self):
        if self.socket is None:
            auth = self.get_auth_socket()
            return Socket(auth)
        return self.socket