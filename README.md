# CryptoMarket
The official Python library for the CryptoMarket API v2

# Installation
To install Cryptomarket, simply use pip:
```
pip install cryptomarket
```
# Documentation

The first things you'll need to do is [sign up in CryptoMarket](https://www.cryptomkt.com/account/register).

## API Key + Secret
If you're writing code for your own CryptoMarket account, [enable an API key](https://www.cryptomkt.com/account2#api_tab).

Next, you'll need to import Client like this:

```python
from cryptomarket.exchange.client import Client
```
Finally, you can 
instantiate the class with the required arguments:
```python
api_key='AB32B3201'
api_secret='21b12401'
client = Client(api_key, api_secret)
```



# Usage

## Public endpoints

### Get markets
```python
client.get_markets()
```
***Expected Output***
```python
{
  "data": [
    "ETHCLP",
    "ETHARS",
    "ETHEUR",
    "ETHBRL",
    "ETHMXN",
    "XLMCLP",
    "XLMARS",
    "XLMEUR",
    "XLMBRL",
    "XLMMXN",
    "BTCCLP",
    "BTCARS",
    "BTCEUR",
    "BTCBRL",
    "BTCMXN",
    "EOSCLP",
    "EOSARS",
    "EOSEUR",
    "EOSBRL",
    "EOSMXN"
  ]
}
```

### Get ticker
```python

client.get_ticker()

#can recieve market as an optional parameter, in that case will return only the ticker of the specified market.

client.get_ticker(market="XLMCLP")
```

***Expected Output***
```python
{
  "data": [
    {
      "ask": "43.5",
      "bid": "42.3",
      "high": "44.9",
      "last_price": "44.8",
      "low": "41.05",
      "market": "XLMCLP",
      "timestamp": "2020-03-09T19:03:34.762778",
      "volume": "151939.515080441682524"
    }
  ]
}
```


### Get book
```python
#can receive "page" as an optional argument.

client.get_book(market="ETHCLP", type="sell", page=1)
```

***Expected Output***
```python
{
  "data": [
    {
      "amount": "0.5045",
      "price": "167600",
      "timestamp": "2020-03-09T19:10:40.043"
    },
    {
      "amount": "0.4865",
      "price": "167600",
      "timestamp": "2020-03-09T19:12:20.360"
    },
    {
      "amount": "0.1387",
      "price": "167460",
      "timestamp": "2020-03-09T19:08:58.451"
    },
        #...
  ]
}
```

### Get trades
```python
client.get_trades(market="ETHCLP")
```

***Expected Output***
```python
{
  "data": [
    {
      "amount": "0.014669811320754716",
      "market": "ETHCLP",
      "market_taker": "buy",
      "price": "169600",
      "timestamp": "2020-03-09T19:25:09"
    },
    {
      "amount": "0.0876",
      "market": "ETHCLP",
      "market_taker": "buy",
      "price": "169600",
      "timestamp": "2020-03-09T19:10:38"
    },
    {
      "amount": "0.471698113207547169",
      "market": "ETHCLP",
      "market_taker": "buy",
      "price": "169600",
      "timestamp": "2020-03-09T19:09:21"
    }
    #...
  ]
}
```

### Get Prices
```python
#"timeframe" value in minutes can be = "1,5,15,60,240,1440,10080".
#can receive "page" and "limit" as optional arguments.

client.get_prices(market="ETHCLP",timeframe=10080)
```

***Expected Output***
```python
{
  "ask": [
    {
      "candle_date": "2020-02-15 12:15",
      "candle_id": 48027,
      "close_price": "227220",
      "hight_price": "227280",
      "low_price": "227220",
      "open_price": "227280",
      "tick_count": "11",
      "volume_sum": "227220"
    },
    {
      "candle_date": "2020-02-15 12:14",
      "candle_id": 48026,
      "close_price": "227300",
      "hight_price": "227340",
      "low_price": "227300",
      "open_price": "227340",
      "tick_count": "3",
      "volume_sum": "227300"
    },
   #...
  ],
  "bid": [
    {
      "candle_date": "2020-03-09 19:49",
      "candle_id": 332723,
      "close_price": "167220",
      "hight_price": "167280",
      "low_price": "167220",
      "open_price": "167280",
      "tick_count": "2",
      "volume_sum": "0"
    },
    {
      "candle_date": "2020-03-09 19:48",
      "candle_id": 332701,
      "close_price": "167400",
      "hight_price": "167500",
      "low_price": "167280",
      "open_price": "167500",
      "tick_count": "3",
      "volume_sum": "0"
    },
 #...
  ]
}
```
## Authenticated enpoints

### Get account 
```python
client.get_account();
```

***Expected Output***
```python
{
  "bank_accounts": [
    {
      "agency": "",
      "bank": "BANCO DEL ESTADO DE CHILE",
      "clabe": "",
      "country": "CL",
      "description": "",
      "dv": "",
      "id": 00000,
      "number": "123456789"
    }
  ],
  "blocked_withdrawals": false,
  "deposit_debts": {
    "BTC": "0",
    "EOS": "0",
    "ETH": "0",
    "XLM": "0"
  },
  "email": "juan.rojas@gmail.com",
  "name": "Juan Rojas",
  "rate": {
    "market_maker": "0.0039",
    "market_taker": "0.0068"
  }
}
```

### Get Active Orders
```python
#can receive page and limit as optional parameters.

client.get_active_orders(market="ETHCLP")
```

***Expected Output***
```python
{
  "data": [
    {
      "amount": {
        "original": "1",
        "remaining": "1"
      },
      "created_at": "2020-03-09T20:41:58.146000",
      "execution_price": null,
      "id": "O1734261",
      "market": "XLMCLP",
      "price": "100",
      "status": "active",
      "type": "sell",
      "updated_at": "2020-03-09T20:41:58.212557"
    },
    #...
  ]
}
```

### Get Executed Orders
```python
#can receive page and limit as optional parameters.

client.get_executed_orders(market="XLMCLP")
```

***Expected Output***
```python
{
  "data": [
    {
      "amount": {
        "executed": "1",
        "original": "1"
      },
      "created_at": "2020-03-09T21:55:26.096000",
      "executed_at": "2020-03-09T21:55:26",
      "execution_price": "43.45",
      "fee": "0.295",
      "id": "O0000001",
      "market": "XLMCLP",
      "price": "40",
      "status": "executed",
      "type": "sell"
    },
    {
      "amount": {
        "executed": "1",
        "original": "1"
      },
      "created_at": "2020-03-05T22:19:41.317000",
      "executed_at": "2020-03-06T03:20:48",
      "execution_price": "49.9",
      "fee": "0.194",
      "id": "O0000002",
      "market": "XLMCLP",
      "price": "49.9",
      "status": "executed",
      "type": "sell"
    },
    #...
  ]
}
```

### Create Order
```python
#"price" is an optional argument, is required only if "type" is "limit" or "stop-limit".

#"limit" is an optional argument, is required only if "type" is "stop-limit".

#"type" can be "limit", "stop-limit" or "market".


client.create_order(market="XLMCLP", type="limit", amount="1", price=50, side="sell")
```

***Expected Output***
```python
{
  "amount": {
    "executed": "0",
    "original": "1"
  },
  "avg_execution_price": "0",
  "created_at": "2020-03-09T23:07:35.185000",
  "fee": "0",
  "id": "O0000001",
  "market": "XLMCLP",
  "price": "50",
  "side": "sell",
  "status": "queued",
  "stop": null,
  "type": "limit",
  "updated_at": "2020-03-09T23:07:35.234007"
}
```

### Get Status of an Order
```python
client.get_order_status(id="O0000001")
```

***Expected Output***
```python
{
  "amount": {
    "executed": "0",
    "original": "1"
  },
  "avg_execution_price": "0",
  "created_at": "2020-03-09T23:07:35.185000",
  "fee": "0",
  "fills": [],
  "id": "O0000001",
  "market": "XLMCLP",
  "price": "50",
  "side": "sell",
  "status": "queued",
  "stop": null,
  "type": "limit",
  "updated_at": "2020-03-09T23:07:35.234007"
}
```

### Cancel an order
```python
client.cancel_order()
```

***Expected Output***
```python
{
  "amount": {
    "executed": "0",
    "original": "1"
  },
  "avg_execution_price": "0",
  "created_at": "2020-03-09T23:07:35.185000",
  "fee": "0",
  "id": "O0000001",
  "market": "XLMCLP",
  "price": "50",
  "side": "sell",
  "status": "cancelled",
  "stop": null,
  "type": "limit",
  "updated_at": "2020-03-11T19:27:28.625385"
}
```

### Get Balance
```python
client.get_balance()
```
***Expected Output***
```python
{
  "data": [
    {
      "available": "0",
      "balance": "0",
      "currency_big_name": "Peso Chileno",
      "currency_decimal": 0,
      "currency_postfix": "",
      "currency_prefix": "$",
      "wallet": "CLP"
    },
    {
      "available": "0",
      "balance": "0",
      "currency_big_name": "Peso Argentino",
      "currency_decimal": 2,
      "currency_postfix": "",
      "currency_prefix": "$",
      "wallet": "ARS"
    },
    {
      "available": "0.0052612795",
      "balance": "0.0052612795",
      "currency_big_name": "Real Brasile\u00f1o",
      "currency_decimal": 2,
      "currency_postfix": "",
      "currency_prefix": "R$",
      "wallet": "BRL"
    },
   #...
  ]
}
```

### Get Transactions
```python
#can recieve "page" and "limit" as optional arguments

client.get_transactions(currency="CLP")
```

***Expected Output***
```python
{
  "data": [
    {
      "address": null,
      "amount": "43.45",
      "balance": "735.98669",
      "blocks": null,
      "currency": "CLP",
      "date": "2020-03-09T21:55:26",
      "fee_amount": "0.295",
      "fee_percent": "0+0.680%",
      "hash": null,
      "id": "T000001",
      "memo": null,
      "type": 1
    },
    {
      "address": null,
      "amount": "49.9",
      "balance": "692.83215",
      "blocks": null,
      "currency": "CLP",
      "date": "2020-03-06T03:20:48",
      "fee_amount": "0.194",
      "fee_percent": "0+0.390%",
      "hash": null,
      "id": "T000002",
      "memo": null,
      "type": 1
    },
 #...
  ]
}
```

### Notify Deposit
```python
#"bank_account" receives the bank account id as a string, you can obtain de id using "get_account()"

client.notify_deposit(bank_account="12345", amount="10000")
```

***Expected Output***
```python
{
  "data": "",
  "pagination": null
}
```

### Notify Withdrawal
```python
#"bank_account" receives the bank account id as a string, you can obtain this id using "client.get_account()".

client.notify_withdrawal(bank_account="12345", amount="10000")
```

***Expected Output***
```python
{
  "data": "",
  "pagination": null
}
```
### Transfer
```python
#can receive "memo" as an optional argument.
client.transfer(address="",amount=0.02,currency="ETH")
```

***Expected Output***
```python
{ status: 'success', data: '' }
```
### Create Multiple Orders
```python
#arguments are the same as regular create_order, but must be contained inside an array of dictionaries
client.create_multi_orders([{Order1},{Order2}])
```
***Expected Output***
```javascript
{
  "created": [
    {
      "data": {
        "amount": {
          "executed": "0",
          "original": "1"
        },
        "avg_execution_price": "0",
        "created_at": "2020-03-13T21:08:31.136000",
        "fee": "0",
        "id": "O0000001",
        "market": "XLMCLP",
        "price": "10",
        "side": "buy",
        "status": "queued",
        "stop": null,
        "type": "limit",
        "updated_at": "2020-03-13T21:08:31.160129"
      },
      "original": {
        "amount": 1,
        "market": "XLMCLP",
        "price": 10,
        "side": "buy",
        "type": "limit"
      }
    },
    {
      "data": {
        "amount": {
          "executed": "0",
          "original": "2"
        },
        "avg_execution_price": "0",
        "created_at": "2020-03-13T21:08:31.218000",
        "fee": "0",
        "id": "O0000001",
        "market": "XLMCLP",
        "price": "10",
        "side": "buy",
        "status": "queued",
        "stop": null,
        "type": "limit",
        "updated_at": "2020-03-13T21:08:31.257744"
      },
      "original": {
        "amount": 2,
        "market": "XLMCLP",
        "price": 10,
        "side": "buy",
        "type": "limit"
      }
    }
  ],
  "not_created": []
}
```

### Cancel Multiple Orders
```python
#cancel_multiple_orders receives an array of dictionaries, those must contain the IDs of your active orders.
client.cancel_multi_orders([{"id":"O0000001"},{"id":"O0000002"}])
```
***Expected Output***
```javascript
{
  "canceled": [
    {
      "data": {
        "amount": {
          "executed": "0",
          "original": "1"
        },
        "avg_execution_price": "0",
        "created_at": "2020-03-13T20:03:07.204000",
        "fee": "0",
        "id": "O0000001",
        "market": "XLMCLP",
        "price": "10",
        "side": "buy",
        "status": "cancelled",
        "stop": null,
        "type": "limit",
        "updated_at": "2020-03-13T20:05:20.971205"
      },
      "order_id": "O0000001"
    },
    {
      "data": {
        "amount": {
          "executed": "0",
          "original": "2"
        },
        "avg_execution_price": "0",
        "created_at": "2020-03-13T20:21:53.991000",
        "fee": "0",
        "id": "O0000002",
        "market": "XLMCLP",
        "price": "10",
        "side": "buy",
        "status": "cancelled",
        "stop": null,
        "type": "limit",
        "updated_at": "2020-03-13T21:00:11.071641"
      },
      "order_id": "O0000002"
    }
  ],
  "not_canceled": []
}
```

## Using Socket

To get a Socket connection with CryptoMarket you'll want to use:

```python
client.get_socket()
```

Note that **some Socket events requires subscription to a _Market Pair_ to work**, you can do it like this:

```python
socket.subscribe('ETHCLP')
```

**Undo subscription**
```python
socket.unsubscribe('ETHCLP')
```

Now you're ready to start receiving Socket events!

### Listening Socket events
```python
socket.on(event, handler)
```
As you can see, **socket.on** receives two arguments, first you need to provide an event name such as **_"open-book"_**, then you can call a handler function to, for example, print the data when it reaches you.

**Handler example**

```python
from __future__ import print_function
import json

def handler(data):
    print(json.dumps(data, indent= 1))
```

### Available Socket events

**Receive open book info**
```python
socket.on('open-book', handler)
```
Output:
```javascript
open-book {
  ETHCLP: {
    sell: [
      [Order1], [Order2],...
    ],
    buy: [
      [Order1], [Order2],...
    ]
  }
}
```

**Receive Historical book info**
```python
socket.on('historical-book', handler)
```
Output:
```javascript
[
    ETHCLP:
{
      requestId: 'OOETHCLP0000000000000000000001',
      tradeId: 'O232937',
      stockId: 'ETHCLP',
      kind: 1,
      type: 2,
      side: 1,
      price: '204820.000000000000000000000000000000',
      limit: null,
      condition: null,
      flag: 'GENERAL',
      amount: '0.00000000000000000000000000000000000',
      initAmount: '2.07330000000000000000000000000000000',
      dateReceived: 1582205310697,
      executed_price: '204820.000000000000000000000000000000',
      executed_amount: '2.07330000000000000000000000000000000',
      executed_date: 1582205310745
    },
    {
      requestId: 'OOETHCLP0000000000000000000002',
      tradeId: 'O232665',
      stockId: 'ETHCLP',
      kind: 1,
      type: 2,
      side: 1,
      price: '201540.000000000000000000000000000000',
      limit: null,
      condition: null,
      flag: 'GENERAL',
      amount: '1.66960000000000000000000000000000000',
      initAmount: '1.92640000000000000000000000000000000',
      dateReceived: 1582204925623,
      executed_price: '201260.000000000000000000000000000000',
      executed_amount: '0.256800000000000000000000000000000000',
      executed_date: 1582204925645
    }
  ]
```

**Receive Candles info**
```python
socket.on('candles', handler)
```
Output:
```javascript
candles: {
  'buy': {
    '1': [
        [{
      date: '21/02/2020 04:56:00',
      stockId: 'ETHCLP',
      type: 1,
      timeFrame: 1,
      lowPrice: 212060,
      hightPrice: 212060,
      openPrice: 212060,
      closePrice: 212100,
      count: 3,
      volume: 0,
      lastBuyPrice: 217900,
      lastSellPrice: 227220
    }],[Object],...],
  '5': [[Object],[Object],...],
  '15':[[Object],[Object],...],
  '60': [[Object],[Object],...],
  '240':[[Object],[Object],...],
  '1440':[[Object],[Object],...],
  '10080':[[Object],[Object],...],
  '44640':[[Object],[Object],...]
}

'sell':{
  '1':[[Object],...],
  '5':...
},
lastBuyPrice: 218880,lastSellPrice: 227220
}
```

**Receive Ticker info**
```python
socket.on('ticker', handler)
```
Output:
```javascript
ticker: {
  EOSARS: {
    BID: 346.95,
    ASK: 364.65,
    delta1d: -13.04511278195489,
    delta7d: -21.928442844284426
  },
  BTCCLP: {
    BID: 7914600,
    ASK: 8038600,
    delta1d: -2.4334319526627217,
    delta7d: -2.1318164956102383
  },
  ETHCLP: {
    BID: 213600,
    ASK: 218880,
    delta1d: 1.0598031794095382,
    delta7d: 0.6692430954849656
  },
  ...
}
```

**Receive Balance info**
```python
socket.on('balance', handler)
```
Output:
```javascript
balance: {
  ETH: {
    currency: 'ETH',
    countable: '0.0700000000000000000000000000000000000',
    available: '0.0700000000000000000000000000000000000',
    currency_kind: 1,
    currency_name: 'ETH',
    currency_big_name: 'Ether',
    currency_prefix: '',
    currency_postfix: ' ETH',
    currency_decimals: 4
  },
  ...
}
```

**Receive Your Open Orders info**
```python
socket.on('open-orders', handler)
```
Output:
```javascript
open-orders [
  {
    requestId: 'OOXLMCLP0000000000000000000001',
    tradeId: 'O000001',
    traderId: '2',
    stockId: 'XLMCLP',
    kind: 2,
    type: 2,
    side: 2,
    price: '80.0000000000000000000000000000000000',
    limit: null,
    condition: null,
    flag: 'GENERAL',
    amount: '1.00000000000000000000000000000000000',
    initAmount: '1.00000000000000000000000000000000000',
    dateReceived: 1582301424510
  },
  {Order2},...
]
```

**Receive Your Historical orders**
```python
socket.on('historical-orders', handler)
```
Output:
```javascript
historical-orders [
  {
    requestId: 'OOXLMCLP000000000000000000001',
    tradeId: 'O000001',
    traderId: '1',
    stockId: 'XLMCLP',
    kind: 2,
    type: 2,
    side: 2,
    price: '50.5000000000000000000000000000000000',
    limit: null,
    condition: null,
    flag: 'GENERAL',
    amount: '0.00000000000000000000000000000000000',
    initAmount: '1.00000000000000000000000000000000000',
    dateReceived: 1582261738700
  },
  {Order2},...
  ]
```
**Receive Your Operated Volume**
```python
socket.on('operated', handler)
```
Output:
```javascript
operated {
  flag: 'L0',
  threshold: '0.00000000000000000000000000000000000',
  traded: '0.0718085391503182500000000000000000000',
  tk: '0.00680000000000000000000000000000000000',
  mk: '0.00390000000000000000000000000000000000'
}
```


