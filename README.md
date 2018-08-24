# CryptoMarket
The official Python library for the [CryptoMarket API v1](https://developers.cryptomkt.com).

# Installation
To install Cryptomarket, simply use pip:
```
pip install cryptomarket
```
# Documentation

The first things you'll need to do is [sign up with CryptoMarket](https://www.cryptomkt.com/account/register).

## API Key + Secret
If you're writing code for your own CryptoMarket account, [enable an API key](https://www.cryptomkt.com/account2#api_tab).

Next, create a Client object for interacting with the API:

```
from cryptomarket.exchange.client import Client

client = Client(api_key, api_secret)
```

# Usage

## [Public endpoints](https://developers.cryptomkt.com/es/#endpoints-publicos)

### Get markets
```
client.get_markets()
```

### Get ticker
```
client.get_ticker(market="ETHCLP")
```

### Get book
```
client.get_book(market="ETHCLP", type="buy")
client.get_book(market="ETHCLP", type="sell")
```

### Get trades
```
client.get_trades(market="ETHCLP")
```