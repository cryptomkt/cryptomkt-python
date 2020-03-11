# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import six


def new_api_object(client, obj, cls=None, **kwargs):
    if isinstance(obj, dict):
        if not cls:
            resource = obj.get('resource', None)
            cls = _resource_to_model.get(resource, None)
        if not cls:
            obj_keys = set(six.iterkeys(obj))
            for keys, model in six.iteritems(_obj_keys_to_model):
                if keys <= obj_keys:
                    cls = model
                    break
        cls = cls or APIObject
        result = cls(client, **kwargs)
        for k, v in six.iteritems(obj):
            result[k] = new_api_object(client, v)
        return result
    if isinstance(obj, list):
        return [new_api_object(client, v, cls) for v in obj]
    return obj


class APIObject(dict):
    __api_client = None
    __response = None
    pagination = None
    __warnings = None

    def __init__(self, api_client, response=None, pagination=None, warnings=None):
        self.__api_client = api_client
        self.__response = response
        self.pagination = pagination
        self.__warnings = warnings

    @property
    def api_client(self):
        return self.__api_client

    @property
    def response(self):
        return self.__response

    @property
    def warnings(self):
        return self.__warnings


    def refresh(self, **params):
        url = getattr(self, 'resource_path', None)
        if not url:
            raise ValueError("Unable to refresh: missing 'resource_path' attribute.")
        response = self.api_client._get(url, data=params)
        data = self.api_client._make_api_object(response, type(self))
        self.update(data)
        return data

    # The following three method definitions allow dot-notation access to member
    # objects for convenience.

    def __getattr__(self, *args, **kwargs):
        try:
            return dict.__getitem__(self, *args, **kwargs)
        except KeyError as key_error:
            attribute_error = AttributeError(*key_error.args)
            attribute_error.message = key_error.message
            raise attribute_error

    def __delattr__(self, *args, **kwargs):
        try:
            return dict.__delitem__(self, *args, **kwargs)
        except KeyError as key_error:
            attribute_error = AttributeError(*key_error.args)
            attribute_error.message = key_error.message
            raise attribute_error

    def __setattr__(self, key, value):
        # All attributes that start with '_' will not be accessible via item-getter
        # syntax, which means that they won't be included in conversion to a
        # vanilla dict, which means that APIObjects can be treated as equivalent to
        # dicts. This is nice because it allows direct JSON-serialization of any
        # APIObject.
        if key.startswith('_') or key in self.__dict__:
            return dict.__setattr__(self, key, value)
        return dict.__setitem__(self, key, value)

    # When an API response includes multiple items, allow direct accessing that
    # data instead of forcing additional attribute access. This works for
    # slicing and index reference only.

    def __getitem__(self, key):
        data = getattr(self, 'data', None)
        if isinstance(data, list) and isinstance(key, (int, slice)):
            return data[key]
        return dict.__getitem__(self, key)

    def __dir__(self):  # pragma: no cover
        # This makes tab completion work in interactive shells like IPython for all
        # attributes, items, and methods.
        return list(self.keys())

    def __str__(self):
        try:
            return json.dumps(self, sort_keys=True, indent=2)
        except TypeError:
            return '(invalid JSON)'

    def __name__(self):
        return '<{0} @ {1}>'.format(type(self).__name__, hex(id(self)))  # pragma: no cover

    def __repr__(self):
        return '{0} {1}'.format(self.__name__(), str(self))  # pragma: no cover


class Order(APIObject):
    def get_active(self, market, page=None, limit=None):
        """get_active_orders(market, **kwargs) -> Order

        https://developers.cryptomkt.com/es/#ordenes-activas

        This method returns the active order lists in CryptoMarket that belong to
        the owner provided in the client.

        List of arguments:
                Required: market
                Optional: page, limit
        """
        return self._get_active_orders(market, page, limit)
    def get_executed(self, market, page=None, limit=None):
        """get_executed_orders(market, **kwargs) -> Order

        https://developers.cryptomkt.com/es/#ordenes-activas
        
        This method returns an executed order list in CryptoMarket that belongs to
        the owner provided in the client.

        List of arguments: 
                Required: market
                Optional: page, limit
        """
        return self._get_executed_orders(market, page, limit)
    
    def get_status(self, id):
        """get_status_order(id) -> Order
        
        https://developers.cryptomkt.com/es/?python#estado-de-orden
        
        This method returns the order state of the provided id.
 
        List of arguments:
                Required: id
                This method does not accept any optional args.
        """
        return self._get_status_order(id)
    def cancel(self, id):
        """cancel_order(id) -> Order
        
        https://developers.cryptomkt.com/es/?python#cancelar-una-orden
        
        This method cancels an order.

        You can access the data given this way:
        order.cancel_order()["fieldYouWant"]

        List of arguments:
                Required: id
                This method does not accept any optional args.
        """
        return self._cancel_order(id)
    
    def get_instant(self,market,type, amount):
        """get_instant(market,type,amount) -> Order
        
        https://developers.cryptomkt.com/es/#obtener-cantidad
        
        This method returns, according to the actual market state, the amount in local
        currency or cryptocurrency if a buy or sell is executed.

        You can access the data this way too:
        order.get_instant(args...)["fieldYouWant"]

        List of arguments:
                required: market, type, amount
                This method does not accept any optional args. 
        """
        return self._get_instant(market, type, amount)

# The following dicts are used to automatically parse API responses into the
# appropriate Python models. See `new_api_object` for more details.
_resource_to_model = {
    #     'account': Account,
    #     'balance': Money,
    #     'buy': Buy,
    #     'checkout': Checkout,
    #     'deposit': Transfer,
    #     'merchant': Merchant,
    #     'notification': Notification,
    #     'order': Order,
    #     'payment_method': PaymentMethod,
    #     'sell': Sell,
    #     'transaction': Transaction,
    #     'transfer': Transfer,
    #     'user': User,
    #     'withdrawal': Withdrawal,
    'order': Order
}

_obj_keys_to_model = {
    #     frozenset(('amount', 'currency')): Money,
}
