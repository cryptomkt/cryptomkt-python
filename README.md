# CryptoMarket-Python

[main page](https://www.cryptomkt.com/)

[sign up in CryptoMarket](https://www.cryptomkt.com/account/register).

# Installation

To install Cryptomarket use pip

```
pip install cryptomarket
```

# Documentation

This sdk makes use of the [api version 3](https://api.exchange.cryptomkt.com) of cryptomarket

# Quick Start

## rest client

```python
from cryptomarket.client import Client
from cryptomarket.args import Account, Side, OrderType
from cryptomarket.exceptions import CryptomarketSDKException

# instance a client
api_key='AB32B3201'
api_secret='21b12401'
client = Client(api_key, api_secret)

# get currencies
currencies = client.get_currencies()

# get order books
order_book = client.get_order_book_of_symbol('EOSETH')

# get your wallet balances
wallet_balance = client.get_wallet_balances()

# get your spot trading balances
trading_balance = client.get_spot_trading_balances()

# move balance from wallet account to trading account
transfer = client.transfer_between_wallet_and_exchange('ETH', '3.2', source=Account.WALLET, destination=Account.SPOT)

# get your active spot orders
orders = client.get_all_active_spot_orders('EOSETH')

# create a new spot order
order = client.create_spot_order('EOSETH', Side.BUY, '10', type=OrderType.MARKET)
```

## Websocket Clients

there are three websocket clients, `MarketDataClient`, the `TradingClient` and the `WalletClient`. The `MarketDataClient` is public, while the others require authentication to be used.

Some subscription callbacks take a second argument, indicating the type of notification, either 'snapshsot' or 'update'.

### MarketDataClient

There are no unsubscriptions methods for the `MarketDataClient`. To stop recieving messages is recomended to close the `MarketDataClient`.

```python
# instance a client
client = MarketDataClient()
client.connect()

# subscribe to public trades
def trades_callback(trades_by_symbol: Dict[str, List[WSTrade]], notification_type):
    for symbol in trades_by_symbol:
        trade_list = trades_by_symbol[symbol]
        for trade in trade_list:
            print(trade)
client.subscribe_to_trades(
  callback=trades_callback,
  symbols=['ETHBTC'],
  limit=5,
)

# subscribe to symbol tickers
def ticker_callback(tikers_of_symbol: Dict[str, WSTicker]):
    for symbol in tikers_of_symbol:
        ticker = tikers_of_symbol[symbol]
        print(ticker)
client.subscribe_to_ticker(
    callback=ticker_callback,
    speed=TickerSpeed._3_SECONDS,
    result_callback=lambda err, result: print(f'err:{err}, result:{result}')
)

# run for some time
time.sleep(10)

# close the client
client.close()
```

### TradingClient

```python
# instance a client with a 15 seconds window
client = TradingClient(api_key, api_secret, window=15_000)
client.connect()
# close the client
client.close()

# subscribe to order reports
def print_feed(feed, feed_type):
    for report in feed:
        print(report)
client.subscribe_to_reports(callback)
# unsubscribe from order reports
client.unsubscribe_to_reports()

client_order_id = str(int(time.time()*1000))

# create an order
client.create_spot_order(
  client_order_id=client_order_id,
  symbol='EOSETH',
  side='sell',
  quantity='0.01',
  price='10000',
)

# candel an order
client.cancel_spot_order(client_order_id)

```

### WalletClient

```python
# instance a client
client = WalletClient(api_key, api_secret)
client.connect()

# close the client
client.close()

# subscribe to wallet transactions
def callback(transaction):
  print(transaction)
client.subscribe_to_transactions(callback)

# unsubscribe from wallet transactions
err = client.unsubscribe_to_transactions()

# get wallet balances
def callback(err, balances):
  if err:
      print(err)
      return
  print(balances)
client.get_wallet_balances(callback)
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


client = WalletClient(api_key, api_secret)
try:
  client.connect()
except Exception as e:
  # here we are catching connection and authentication errors
  print(e)
```

websocket methods take callbacks with two parameters, the first is the possible error, the second is the result of response from the server, for example:

```python
def callback(err, balances):
  if err:
      print(err)
      return
  print(balances)
client.get_wallet_balances(callback)
```

websocket subscriptions also have this type of callback, but is called **result_callback** instead

## Constants of interest

All constants required for calls are in the `cryptomarket.args` module.

## Dataclasses

All classes returned by the client are in the `cryptomarket.dataclasses` module

# Checkout our other SDKs

[node sdk](https://github.com/cryptomkt/cryptomkt-node)

[java sdk](https://github.com/cryptomkt/cryptomkt-java)

[go sdk](https://github.com/cryptomkt/cryptomkt-go)

[ruby sdk](https://github.com/cryptomkt/cryptomkt-ruby)
