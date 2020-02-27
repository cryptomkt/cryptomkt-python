# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import warnings

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
        """get_markets(self) -> APIObject
        
        https://developers.cryptomkt.com/es/#mercado
        
        This method returns the markets available in CryptoMarket. 
        You can access them by client.get_markets[indexYouWant]. 
        
        This method does not need any arguments"""
        response = self._get(self.API_VERSION, 'market')
        return self._make_api_object(response, APIObject)

    def get_ticker(self, market=None):
        """get_ticker(self) -> APIObject

        https://developers.cryptomkt.com/es/#obtener-ticker
        
        The ticker is a high level general view market state. It will show you
        the actual bid and ask as well as the last price market. Besides, it 
        includes information like daily volume and how much it has changed through 
        the day.

        You can access the data this way too: 
        client.get_ticker(args...)[indexYouWant]["fieldYouWant"]

        List of arguments:
                Required: None
                Optional: market (string)
        """
        params = {}

        if market:
            params['market'] = market

        response = self._get(self.API_VERSION, 'ticker', params=params)
        return self._make_api_object(response, APIObject)

    def get_book(self, market, type, page=None, limit=None):
        """get_book(self, market, type, **kwargs) -> APIObject
        
        https://developers.cryptomkt.com/es/#libro-de-ordenes
        
        This method returns the orders book according to the market and type provided.

        You can access the data this way too:
        client.get_book(args...)[indexYouWant]["fieldYouWant"]

        List of arguments: 
                Required: market (string), type (string)
                Optional: page (int), limit (int)
        """
        params = dict(
            market=market,
            type=type
        )

        if page and isinstance(page, int):
            params['page'] = page

        if limit and isinstance(limit, int):
            params['limit'] = limit

        response = self._get(self.API_VERSION, 'book', params=params)
        return self._make_api_object(response, APIObject)

    def get_trades(self, market, start=None, end=None, page=None, limit=None):
        """get_trades(self, market, **kwargs) -> APIObject
        
        https://developers.cryptomkt.com/es/#obtener-trades
        
        This method returns the done trades in CryptoMarket. 

        You can access the data this way too:
        client.get_trades(args...)[indexYouWant]["fieldYouWant"]

        List of arguments:
                Required: market (string)
                Optional: start (string YYYY-MM-DD), end (string YYYY-MM-DD), page (int), limit (int)

        """
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

        response = self._get(self.API_VERSION, 'trades', params=params)
        return self._make_api_object(response, APIObject)

    def get_prices(self, market, timeframe, page = None, limit = None):
        """get_prices(market, timeframe, **kwargs) -> APIObject
        
        https://developers.cryptomkt.com/es/#precios

        This method returns the displayed data in the Market section in CryptoMarket

        You can access the data this way too:
        client.get_prices(args...)["ask or bid (choose one)"][indexYouWant]

        List of arguments:
                Required: market (string), timeframe (string)
                Optional: page (int), limit (int)
        """
        params = dict(
            market = market,
            timeframe = timeframe
        )
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit

        response = self._get(self.API_VERSION,"prices", params = params)
        return self._make_api_object(response, APIObject)

    # Authenticated API
    #-------------------------------------------------------------------
    # account 
    def get_account(self):
        """get_account() -> APIObject

        https://developers.cryptomkt.com/es/#informacion-de-cuenta

        This method displays your account info.

        You can access the info this way:
        client.get_account()["fieldYouWant"]

        This method does not require any arguments

        """
        response = self._get(self.API_VERSION,"account")
        return self._make_api_object(response,APIObject)

    # orders
    def _get_active_orders(self, market, page=None, limit=None):
        """get_active_orders(market, **kwargs) -> Order

        https://developers.cryptomkt.com/es/#ordenes-activas

        This method returns the active order lists in CryptoMarket that belong to
        the owner provided in the client.

        List of arguments:
                Required: market (string)
                Optional: page (int), limit (int)
        """
        params = dict(
            market=market
        )

        if page:
            params['page'] = page

        if limit:
            params['limit'] = limit

        response = self._get(self.API_VERSION, 'orders', 'active', params=params)
        return self._make_api_object(response, Order)

    def _get_executed_orders(self, market, page=None, limit=None):
        """get_executed_orders(market,**kwargs) -> Order

        https://developers.cryptomkt.com/es/#ordenes-activas
        
        This method returns an executed order list in CryptoMarket that belongs to
        the owner provided in the client.

        List of arguments: 
                Required: market (string)
                Optional: page (int), limit (int)
        """
        params = dict(
            market=market
        )

        if page:
            params['page'] = page

        if limit:
            params['limit'] = limit

        response = self._get(self.API_VERSION, 'orders', 'executed', params=params)
        return self._make_api_object(response, Order)

    def create_order(self, market, amount, price, type):
        """create_order(market, amount, price) -> Order
        
        https://developers.cryptomkt.com/es/?python#crear-orden
        
        This method lets you create an sell or buy order inside CryptoMarket. 

        You can access the data this way too:
        client.create_order(args...)["fieldYouWant"]

        List of arguments:
                Required: market (string), amount (string), price (string), type (string)
                This method does not accept any optional args.
        """
        params = dict(
            market=market,
            amount=amount,
            price=price,
            type=type
        )

        response = self._post(self.API_VERSION, 'orders', 'create', data=params)
        return self._make_api_object(response, Order)

    def _get_status_order(self, id):
        """get_status_order(id) -> Order
        
        https://developers.cryptomkt.com/es/?python#estado-de-orden
        
        This method returns the order state of the provided id.
 
        List of arguments:
                Required: id (string)
                This method does not accept any optional args.
        """
        params = dict(
            id=id
        )

        response = self._get(self.API_VERSION, 'orders', 'status', params=params)
        return self._make_api_object(response, Order)

    def _cancel_order(self, id):
        """cancel_order(id) -> Order
        
        https://developers.cryptomkt.com/es/?python#cancelar-una-orden
        
        This method cancels an order.

        You can access the data given this way:
        order.cancel_order()["fieldYouWant"]

        List of arguments:
                Required: id (string)
                This method does not accept any optional args.
        """
        params = dict(
            id=id
        )

        response = self._post(self.API_VERSION, 'orders', 'cancel', data=params)
        return self._make_api_object(response, Order)
    
    def _get_instant(self,market,type, amount):
        """get_instant(market,type,amount) -> Order
        
        https://developers.cryptomkt.com/es/#obtener-cantidad
        
        This method returns, according to the actual market state, the amount in local
        currency or cryptocurrency if a buy or sell is executed.

        You can access the data this way too:
        order.get_instant(args...)["fieldYouWant"]

        List of arguments:
                required: market (string), type (string), amount (string)
                This method does not accept any optional args. 
        """
        params = dict(
            market = market,
            type = type,
            amount = amount
        )
        response = self._get(self.API_VERSION, "orders","instant","get", params = params)
        return self._make_api_object(response,Order)
    
    def create_instant(self,market,type,amount):
        """create_instant(market, type, amount) -> Order

        https://developers.cryptomkt.com/es/#crear-orden-2
        
        This method creates a instant sell or buy order inside CryptoMarket Instant Exchange.

        List of arguments:
                Required: market (string), type (string), amount (string)
                This method doen tno accept any optional args.
        """
        params = dict(
            market=market,
            type = type,
            amount = amount
        )
        response = self._post(self.API_VERSION,"order", "instant", "create", data = params)
        return self._make_api_object(response,Order)
    
    #Wallet
    def get_balance(self):
        """get_balance() -> APIObject

        https://developers.cryptomkt.com/es/?python#obtener-balance

        This method returns your actual wallets balances
        
        You can access the data this way too:
        client.get_balance()[indexYouWant]["fieldYouWant"]

        This method does not require any args.
        """

        response = self._get(self.API_VERSION, 'balance')
        return self._make_api_object(response, APIObject)
    
    def get_transactions(self, currency, page = None, limit = None):
        """get_transactions(currency, **kwargs) -> APIObject

        https://developers.cryptomkt.com/es/#obtener-movimientos

        This method returns your actual wallets transactions. 

        You can access the data this way too:
        client.get_transactions(args...)[indexYouWant]["fieldYouWant"]

        List of arguments:
                Required: currency (string)
                Optional: page (int), limit (int)

        """
        params = dict(
            currency = currency
        )

        if page:
            params["page"] = page

        if limit:
            params["limit"] = limit
        
        response = self._get(self.API_VERSION, "transactions", params=params)
        return self._make_api_object(response, APIObject)

    def notify_deposit(self,amount,bank_account, date= None, tracking_code = None, voucher = None):
        """notify_deposit(amount, bank_account, **kwargs) -> APIObject

        https://developers.cryptomkt.com/es/#notificar-deposito
        
        This method notifies a deposit to a local wallet currency.

        List of arguments:
                Required: amount (string), bank_account (string)
                Required for México: date (string dd/mm/yyyy), tracking_code (string), voucher (file)
                Required for Brazil and European Union: voucher (file)
        """
        params = dict(
            amount = amount,
            bank_account = bank_account            
        )
        if date:
            params["date"] = date 
        if tracking_code:
            params["tracking_code"] = tracking_code
        if voucher:
            params["voucher"] = voucher
        
        response = self._post(self.API_VERSION,"request", "deposit", data = params)
        return self._make_api_object(response,APIObject)

    def notify_withdrawal(self, amount, bank_account):
        """notify_withdrawal(amount, bank_account) -> APIObject

        https://developers.cryptomkt.com/es/#notificar-retiro
        
        This method notifies a withdrawal froma local currency wallet

        List of arguments:
                Required: amount (string), bank_account (string)
                This method does not accept any optional args.
        """
        params = dict(
            amount = amount,
            bank_account = bank_account
        )
        response = self._post(self.API_VERSION, "request", "withdrawal", data = params)
        return self._make_api_object(response, APIObject)

    def transfer(self,address, amount, currecy, memo = None):
        """transfer(addres, amount, currency, **kwargs) -> APIObject

        https://developers.cryptomkt.com/es/#transferir
        
        This method tranfers cryptocurrencies to another wallet

        List of arguments:
                Required: address (string), amount (string), currency (string)
                Optional: memo (string)
        """
        params = dict(
            address = address,
            amount = amount,
            currency = currency
        )
        if memo:
            params["memo"] = memo
        
        response = self._post(self.API_VERSION, "transfer", data = params)
        return self._make_api_object(response, APIObject)
    
    def create_wallet(self, id, token, wallet):
        """create_wallet(id,token, wallet) -> APIObject
        
        https://developers.cryptomkt.com/es/#crear-billetera-de-orden-de-pago

        This method creates a cryptocurrency wallet which can pay payments orders

        You can access the data this way too:
        client.create_wallet(args...)["fieldYouWant"]

        List of arguments:
                Required: id (string), token (string), wallet (string)
                This method does not accept any optional args.
        """
        params = dict(
            id=id,
            token=token,
            wallet=wallet,
        )
        response = self._post(self.API_VERSION, "payment/create_wallet", data = params)
        return self._make_api_object(response, APIObject)


    def new_payment_order(self, to_receive, to_receive_currency, payment_receiver, 
        external_id=None, callback_url=None, error_url=None, success_url=None, refund_email=None, language=None):
        """new_payment_order(to_receive,to_receive_currency, payment_receiver, **kwargs) -> APIObject

        https://developers.cryptomkt.com/es/#crear-orden-de-pago
        
        This method creates a payment order, delivering a  QR code and urls for paying.

        List of arguments: 
                Required: to_receive (double), to_receive_currency (string), payment_receiver (string)
                Optional: external_id (string), callback_url (string), error_url (string), 
                          success_url (string), refund_e-mail (string), language(string)

        """
        params = dict(
            to_receive = to_receive,
            to_receive_currency = to_receive_currency,
            payment_receiver = payment_receiver,
            external_id = external_id, 
            callback_url = callback_url, 
            error_url = error_url, 
            success_url = success_url, 
            refund_email = refund_email, 
            language = language
        )

        response = self._post(self.API_VERSION, "payment/new_order", data = params)
        return self._make_api_object(response, APIObject)

    def payment_status(self, id):
        """payment_status(id) -> APIObject
        
        https://developers.cryptomkt.com/es/#estado-de-orden-de-pago
        
        This method returns the payment order state. 
        
        You can access the data this way too:
        client.payment_status(args...)["fieldYouWant"]

        List of arguments:
                Required: id (string)
                This method does not accept any optional args.
        """
        params = dict(
            id = id,
        )
        response = self._get(self.API_VERSION, "payment/status", data = params)
        return self._make_api_object(response, APIObject)

    def payment_orders(self, start_date, end_date, page=None, limit=None):
        """payment_orders(start_date, end_date, **kwargs) -> APIObject
        
        https://developers.cryptomkt.com/es/#listado-de-ordenes-de-pago

        This method returns the generated payment orders. 

        You can access the data this way too:

        List of arguments:
                Required: start_date (string dd/mm/yyyy), end_date (string dd/mm/yyyy)
                Optional: page (int), limit (int) 
        """
        params = dict(
            start_date = start_date,
            end_date = end_date,
            page = page,
            limit = limit,
        )
        response = self._get(self.API_VERSION, "payment/orders", data = params)
        return self._make_api_object(response, APIObject)

    def get_auth_socket(self):
        """get_auth_socket() -> APIObject

        This method returns the data for connecting to websockets, your uid and socid

        This method does not accept any args. 
        """
        response = self._get("v2", "socket/auth")
        return self._make_api_object(response, APIObject)