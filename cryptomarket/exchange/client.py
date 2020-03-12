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
from .socket import Socket


from .compat import imap
from .compat import quote
from .compat import urljoin
from .compat import urlencode


class Client(object):

    BASE_API_URI = 'https://api.cryptomkt.com/'
    API_VERSION = 'v2'

    def __init__(self, api_key, api_secret, base_api_uri=None, api_version=None):
        if not api_key:
            raise ValueError('Missing `api_key`.')
        if not api_secret:
            raise ValueError('Missing `api_secret`.')

            # Allow passing in a different API base.
        self.BASE_API_URI = check_uri_security(base_api_uri or self.BASE_API_URI)

        self.API_VERSION = api_version or self.API_VERSION

        self.socket = None

        # Set up a requests session for interacting with the API.
        self.session = self._build_session(HMACAuth, api_key, api_secret, self.API_VERSION)

        # a container for the socket if needed.
        self.socket = None

    def _build_session(self, auth_class, *args, **kwargs):
        """Internal helper for creating a requests `session` with the correct
        authentication handling."""
        session = requests.session()
        session.auth = auth_class(*args, **kwargs)
        # session.headers.update({'Content-type': 'application/json'})
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

        https://developers.cryptomkt.com/#mercado
        """
        response = self._get(self.API_VERSION, 'market')
        return self._make_api_object(response, APIObject)


    def get_ticker(self, market=None):
        """Returns a general view of the market state as a dict.
        shows the actual bid and ask, also the volume and price, 
        and the low and high. stored in the "data" member of a dict

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


    def get_book(self, market, side, page=None, limit=None):
        """Returns a list of active orders of a given side in a specified
        market pair. stored in the "data" member of a dict

        Required Arguments:
            market: A market pair as a string. Is the specified market to get
                the book from.
                e.g: 'ETHEUR'.
            side: 'buy' or 'sell'.
        Optional Arguments:
            page: Page number to query. Default is 0
            limit: Number of orders returned in each page. Default is 20.

        https://developers.cryptomkt.com/#libro-de-ordenes
        """
        params = dict(
            market=market,
            side=side
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
        older last. stored in the "data" member of a dict
        If no start date is given, returns trades since 2020-02-17.
        If no end date is given, returns trades until the present moment.

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
        """returns a list of the prices of a market (candles on the market 
        prices graph), given a timeframe. The earlier prices first and the 
        older last. the list is stored in the data member of a dict

        Required Arguments:
            market: A market pair as a string. Is the specified market to get
                the book from.
                e.g: 'ETHCLP'.
            timeframe: timelapse between every candle in minutes.
                accepted values are 1, 5, 15, 60, 240, 1440 and 10080.
        Optional Arguments:
            page: Page number to query. Default is 0
            limit: Number of orders returned in each page. Default is 20.

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

    # Authenticated endpoints
    #-------------------------------------------------------------------
    # account 
    def get_account(self):
        """returns the account information of the user. Name, email, rate 
        and bank accounts.

        https://developers.cryptomkt.com/#informacion-de-cuenta
        """
        response = self._get(self.API_VERSION,"account")
        return self._make_api_object(response,APIObject)

    # orders
    def get_active_orders(self, market, page=None, limit=None):
        """returns a list of the active orders of the user in a given market.

        Required Arguments:
            market: A market pair as a string. Is the specified market to get
                the book from.
                e.g: 'ETHCLP'.
        Optional Arguments:
            page: Page number to query. Default is 0
            limit: Number of orders returned in each page. Default is 20.

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
        """returns the list of the executed orders of the user on a given market.

        Required Arguments:
            market: A market pair as a string. Is the specified market to get
                the book from.
                e.g: 'ETHCLP'.
        Optional Arguments:
            page: Page number to query. Default is 0
            limit: Number of orders returned in each page. Default is 20.

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


    def create_order(self, market, amount, price, side, type):
        """creates an orders from the specified argument.

        Required Arguments:
            amount: The amount of crypto to be buyed or selled.
            market: A market pair as a string. Is the specified market to place the order in
                e.g: 'ETHCLP'.
            price: The price to ask or bid for one unit of crypto
            side: 'buy' or 'sell' the crypto
            type: one of the keywords 'market', 'limit', 'stop_limit'
        
        https://developers.cryptomkt.com/#crear-orden
        """
        params = dict(
            amount=amount,
            market=market,
            price=price,
            side=side,
            type=type,
        )

        response = self._post(self.API_VERSION, 'orders', 'create', data=params)
        return self._make_api_object(response, Order)


    def get_order_status(self, id):
        """returns the present status of an order, given the order id.
        
        Required Arguments:
            id: The identification of the order.
        
        https://developers.cryptomkt.com/#estado-de-orden
        """
        params = dict(
            id=id
        )

        response = self._get(self.API_VERSION, 'orders', 'status', params=params)
        return self._make_api_object(response, Order)


    def cancel_order(self, id):
        """Cancel an order given its id.

        Required Arguments:
            id: The identification of the order.

        https://developers.cryptomkt.com/#cancelar-una-orden
        """
        params = dict(
            id=id
        )

        response = self._post(self.API_VERSION, 'orders', 'cancel', data=params)
        return self._make_api_object(response, Order)
    
    def get_instant(self,market, side, amount):
        """If side is sell, returns an estimate of the amount of fiat obtained and the amount of crypto required to obatin it.
        If side is buy, returns an estimate of the amount of crypto obtained and the amount of fiat required to obtain it.

        Required Arguments:
            market: The market to get the estimate of the transaction. 
            side: 'buy' or 'sell'
            amount: Is the amount of crypto to 'buy' or 'sell'

        https://developers.cryptomkt.com/#obtener-cantidad
        """

        rest = float(amount)
        book_side = 'sell' if side == 'buy' else 'buy'
        amount_required = 0.0
        amount_obtained = 0.0
        page = 0
        n_entries = 100
        while True:
            book_page = self.get_book(market, book_side, page=page, limit=n_entries)
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
        
        if book_side == 'sell':
            temp = amount_required
            amount_required = amount_obtained
            amount_obtained = temp
        instant = dict(obtained=amount_obtained, required=amount_required)
        return instant
        
    #Wallet
    def get_balance(self):
        """returns the balance of the user.

        https://developers.cryptomkt.com/#obtener-balance
        """

        response = self._get(self.API_VERSION, 'balance')
        return self._make_api_object(response, APIObject)
    
    def get_transactions(self, currency, page = None, limit = None):
        """return all the transactions of a currency of the user.

        Arguments:
            currency: The currency to get all the user transactions.

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
        """Notifies a deposit from your bank account to your wallet (fiat).

        Arguments:
            amount: The amount deposited to your wallet.
            bank_account: The address (id) of the bank account from which you deposited.

        Arguments required for Brazil and the European Union:
            voucher: a file.

        Arguments required for Mexico:
            date: The date of the deposit, in format dd/mm/yyyy.
            tracking_code: The tracking code of the deposit.
            voucher: a file.
                
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
        
        response = self._post(self.API_VERSION, "deposit", data = params)
        return self._make_api_object(response,APIObject)

    def notify_withdrawal(self, amount, bank_account):
        """Notifies a withdrawal from fiat wallet to your bank account.

        Arguments:
            amount: the amount you need to withdraw to your bank account.
            bank_account: The address(id) of the bank account.

        https://developers.cryptomkt.com/#notificar-retiro
        """
        params = dict(
            amount = amount,
            bank_account = bank_account
        )
        response = self._post(self.API_VERSION, "withdrawal", data = params)
        return self._make_api_object(response, APIObject)

    def transfer(self,address, amount, currency, memo = None):
        """transfer money between wallets.
        
        Arguments:
            adderss: The address of the wallet to transfer money.
            amount: The amount of money to transfer into the wallet.
            currency: The wallet from which to take the money.
                e.g. 'ETH'
            memo (optional): memo of the wallet to transfer money.

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
        """returns the userid and the socket ids to permit a socket connection with cryptomkt.
        """
        response = self._get("v2", "socket/auth")
        return self._make_api_object(response, APIObject)

    
    def get_socket(self):
        """returns a socket connection with cryptomkt.
        """
        if self.socket is None:
            auth = self.get_auth_socket()
            del auth['verify']
            self.socket = Socket(auth)
        return self.socket