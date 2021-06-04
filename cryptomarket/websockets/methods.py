# mapping for caches
mapping = {
    # reports
    'subscribeReports':'reports',
    'activeOrders':'reports',
    'report':'reports',
    # tickers
    'subscribeTicker':'tickers',
    'unsubscribeTicker':'tickers',
    'ticker':'tickers',
    # orderbooks
    'subscribeOrderbook':'orderbooks',
    'unsubscribeOrderbook':'orderbooks',
    'snapshotOrderbook':'orderbooks',
    'updateOrderbook':'orderbooks',
    # trades
    'subscribeTrades':'trades',
    'unsubscribeTrades':'trades',
    'snapshotTrades':'trades',
    'updateTrades':'trades',
    # candles
    'subscribeCandles':'candles',
    'unsubscribeCandles':'candles',
    'snapshotCandles':'candles',
    'updateCandles':'candles',
}

def method_key(method):
    if method not in mapping: return ""
    return mapping[method]

def orderbook_feed(method):
    return method == 'snapshotOrderbook' or method == 'updateOrderbook'

def candles_feed(method):
    return method == 'snapshotCandles' or method == 'updateCandles'

def trades_feed(method):
    return method == 'snapshotTrades' or method == 'updateTrades'