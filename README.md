# CryptoMarket-Python
[main page](https://www.cryptomkt.com/)


[sign up in CryptoMarket](https://www.cryptomkt.com/account/register).

# Installation
To install Cryptomarket use pip
```
pip install cryptomarket
```
# Documentation

This sdk makes use of the [api version 2](https://api.exchange.cryptomkt.com/v2) of cryptomarket


# Quick Start

## rest client
```python
from cryptomarket.client import Client
from cryptomarket.exceptions import CryptomarketSDKException

# instance a client
api_key='AB32B3201'
api_secret='21b12401'
client = Client(api_key, api_secret)

# get currencies
currencies = client.get_currencies()

# get order books
order_book = client.get_order_book('EOSETH')

# get your account balances
account_balance = client.get_account_balance()

# get your trading balances
trading_balance = client.get_trading_balance()

# move balance from account bank to account trading
result = client.transfer_money_from_bank_balance_to_trading_balance('ETH', '3.2')

# get your active orders
orders = client.get_active_orders('EOSETH')

# create a new order
order = client.create_order('EOSETH', 'buy', '10', order_type=args.ORDER_TYPE.MARKET)
```

## websocket client

All websocket calls work with callbacks, subscriptions use a callback with one argument for the subscription feed. All the other callbacks takes two arguments, err and result: callback(err, result). If the transaction is successful err is None and the result is in result. If the transaction fails, result is None and the error is in err.

There are three websocket clients, the PublicClient, the TradingClient and the AccountClient.

```python
from cryptomarket.websocket import PublicClient, TradingClient, AccountClient

# THE PUBLIC CLIENT

wsclient = PublicClient()

wsclient.connect() # blocks until connected

def my_callback(err, data):
    if err is not None: # deal with error
    print(data)

# get currencies
wsclient.get_currencies(my_callback)


# get an order book feed, 
# feed_callback is for the subscription feed, with one argument
# result_callback is for the subscription result (success or failure)
def feed_callback(feed):
    print(feed)

wsclient.subscribe_to_order_book('EOSETH', callback=feed_callback, result_calback=my_callback)

# THE TRADING CLIENT

wsclient = TradingClient(api_key, api_secret)

wsclient.connect() # blocks until connected and authenticated.

# get your trading balances
wsclient.get_trading_balance(my_callback)

# get your active orders
wsclient.get_active_orders(my_callback)

# create a new order
clientOrderId = '123123123'
wsclient.create_order('EOSETH', 'buy', '3', callback=my_callback)

# THE ACCONUT CLIENT

wsclient = AccountClient(api_key, api_secret)

wsclient.connect() # blocks until connected

wsclient.get_account_balance(my_callback)
```


## exception handling
```python
from cryptomarket.client import Client
from cryptomarket.exceptions import CryptomarketSDKException

client = Client(api_key, secret_key)

# catch a wrong argument 
try:
    order = client.create_order(
        symbol='EOSETH', 
        side='selllll', # wrong
        quantity='3'
    )
except CryptomarketSDKException as e:
    print(f'exception catched {e}')

# catch a failed transaction
try:
    order = client.create_order(
        symbol='eosehtt',  # non existant symbol
        side='sell',
        quantity='10', 
    )
except CryptomarketSDKException as e:
    print(f'exception catched {e}')


wsclient = TradingClient(api_key, api_secret)

# websocket errors are passed as the first argument to the callback
def callback(err, result):
    if err is not None:
        print('an error ocurred')
        print(err)
    else:
        print('successful transaction')
        print(result)

wsclient.authenticate(callback=callback)

# catch authorization error
# to catch an authorization error on client connection, a on_error function must be passed to the client
wsclient = TradingClient(apiKey, apiSecret, on_error=lambda err: print(err))
```

# Constants of interest

All constants required for calls are in the `cryptomarket.args` module.
each enum has the name of the argument that needs it.
Here is the full list
```python
import cryptomarket.args as args

args.SORT.ASCENDING = 'ASC'
args.SORT.DESCENDING = 'DESC'

args.BY.TIMESTAMP = 'timestamp'
args.BY.ID = 'id'

args.PERIOD._1_MINS = 'M1'
args.PERIOD._3_MINS = 'M3'
args.PERIOD._5_MINS = 'M5'
args.PERIOD._15_MINS = 'M15'
args.PERIOD._30_MINS = 'M30'
args.PERIOD._1_HOURS = 'H1'
args.PERIOD._4_HOURS = 'H4'
args.PERIOD._1_DAYS = 'D1'
args.PERIOD._7_DAYS = 'D7'
args.PERIOD._1_MONTH = '1M'

args.SIDE.BUY = 'buy'
args.SIDE.SELL = 'sell'

args.ORDER_TYPE.LIMIT = 'limit'
args.ORDER_TYPE.MARKET = 'market'
args.ORDER_TYPE.STOPLIMIT = 'stopLimit'
args.ORDER_TYPE.STOPMARKET = 'stopMarket'

args.TIME_IN_FORCE.GTC = 'GTC' # Good till canceled
args.TIME_IN_FORCE.IOC = 'IOC' # Immediate or cancell
args.TIME_IN_FORCE.FOK = 'FOK' # Fill or kill
args.TIME_IN_FORCE.DAY = 'Day' # Good for the day
args.TIME_IN_FORCE.GTD = 'GDT' # Good till date

args.TRANSFER_BY.USERNAME = 'username',
args.TRANSFER_BY.EMAIL = 'email'
```

# Checkout our other SDKs

[node sdk](https://github.com/cryptomkt/cryptomkt-node)

[java sdk](https://github.com/cryptomkt/cryptomkt-java)

[go sdk](https://github.com/cryptomkt/cryptomkt-go)

[ruby sdk](https://github.com/cryptomkt/cryptomkt-ruby)
