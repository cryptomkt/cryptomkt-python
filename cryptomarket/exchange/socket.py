from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import socketio

from .patch_json import patch

class Socket(object):
    def __init__(self, socketids):
        self.url_worker = 'https://worker.cryptomkt.com'
        self.currencies_data = dict()
        self.balance_data = dict()
        self.operated_data = dict()
        self.open_orders_data = dict()
        self.historical_orders_data = dict()
        self.open_book_data = dict()
        self.historical_book_data = dict()
        self.candles_data = dict()
        self.board_data = dict()

        self.socketids = socketids
        sio =  socketio.Client()

        @sio.event
        def connect():
            print('connected to server')

        @sio.event
        def disconnect():
            print('disconnected from server')

        sio.connect(self.url_worker)
        sio.emit('user-auth', socketids)


        @sio.on('currencies')
        def currencies_handler(data):
            self.currencies_data = data
        
        @sio.on('currencies-delta')
        def currencies_delta_handler(delta):
            if self.currencies_data['to_tx'] != delta['from_tx']:
                sio.emit('currencies')
                return
            patch(self.currencies_data['data'], delta['delta_data'])
            self.currencies_data['to_tx'] = delta['to_tx']
        

        @sio.on('balance')
        def balance_handler(data):
            for _, value in data['data'].items():
                currency = value['currency']
                value.update({
                    'currency_kind':self.currencies_data['data'][currency]['kind'],
                    'currency_name':self.currencies_data['data'][currency]['name'],
                    'currency_big_name':self.currencies_data['data'][currency]['big_name'],
                    'currency_prefix':self.currencies_data['data'][currency]['prefix'],
                    'currency_postfix':self.currencies_data['data'][currency]['postfix'],
                    'currency_decimals':self.currencies_data['data'][currency]['decimals'],
                })
            self.balance_data = data
        
        
        @sio.on('balance-delta')
        def balance_delta_handler(deltas):
            for (delta, index, collection) in deltas:
                if self.balance_data['to_tx'] != delta['from_tx']:
                    sio.emit('balance')
                    return
                patch(self.balance_data['data'], delta['delta_data'])
                self.balance_data['to_tx'] = delta['to_tx']
                if index == len(collection) - 1:
                    for _, value in self.balance_data.items():
                        currency = value['currency']
                        value.update({
                            'currency_kind':self.currencies_data['data'][currency]['kind'],
                            'currency_name':self.currencies_data['data'][currency]['name'],
                            'currency_big_name':self.currencies_data['data'][currency]['big_name'],
                            'currency_prefix':self.currencies_data['data'][currency]['prefix'],
                            'currency_postfix':self.currencies_data['data'][currency]['postfix'],
                            'currency_decimals':self.currencies_data['data'][currency]['decimals'],
                        })


        @sio.on('open-orders')
        def open_orders_handler(data):
            self.open_orders_data = data
            sio.emit('open-orders', data)
        
        @sio.on('open-orders-delta')
        def open_orders_delta_handler(deltas):
            for (delta, index, collection) in deltas:
                if self.open_orders_data['to_tx'] != delta['from_tx']:
                    sio.emit('open-orders')
                patch(self.open_orders_data['data'], delta['delta_data'])
                self.open_orders_data['to_tx'] = delta['to_tx']
                if index == len(collection) - 1:
                    sio.emit('open-orders', self.open_orders_data['data'])


        @sio.on('historical-orders')
        def historical_orders_handler(data):
            self.historical_orders_data = data
            sio.emit('historical-orders', data)
        
        @sio.on('historical-orders-delta')
        def historical_orders_delta_handler(deltas):
            for (delta, index, collection) in deltas:
                if self.historical_orders_data['to_tx'] != delta['from_tx']:
                    sio.emit('historical-orders')
                patch(self.historical_orders_data['data'], delta['delta_data'])
                self.historical_orders_data['to_tx'] = delta['to_tx']
                if index == len(collection) - 1:
                    sio.emit('historical-orders', self.historical_orders_data['data'])


        @sio.on('operated')
        def operated_handler(data):
            self.operated_data = data
            sio.emit('operated', data)
        
        @sio.on('operated-delta')
        def operated_delta_handler(deltas):
            for (delta, index, collection) in deltas:
                if self.operated_data['to_tx'] != delta['from_tx']:
                    sio.emit('operated')
                patch(self.operated_data['data'], delta['delta_data'])
                self.operated_data['to_tx'] = delta['to_tx']
                if index == len(collection) - 1:
                    sio.emit('operated', self.operated_data['data'])


        @sio.on('open-book')
        def open_book_handler(data):
            stock_id = data['stock_id']
            self.open_book_data.update({stock_id:data})
            sio.emit(
                'open-book', 
                {
                    stock_id:{
                        'buy':data['data']['1'],
                        'sell':data['data']['2']}
                }
            )
        
        @sio.on('open-book-delta')
        def open_book_delta_handler(delta):
            stock_id = delta['stock_id']
            if not stock_id in self.open_book_data:
                sio.emit('open-book', {'stockId':stock_id})
                return
            elif self.open_book_data[stock_id]['to_tx'] != delta['from_tx']:
                sio.emit('open-book', {'stock_id':stock_id})

            stock_data = self.open_book_data[stock_id]
            patch(stock_data['data'], delta['delta_data'])
            stock_data['to_tx'] = delta['to_tx']
            sio.emit(
                'open-book', 
                {
                    stock_id:{
                        'buy':stock_data['data']['1'],
                        'sell':stock_data['data']['2']}
                }
            )


        @sio.on('historical-book')
        def historical_book_handler(data):
            stock_id = data['stock_id']
            self.historical_book_data.update({stock_id:data})
            sio.emit(
                'historical-book',
                {stock_id:data['data']}
            )
        
        @sio.on('historical-book-delta')
        def historical_book_delta_handler(delta):
            stock_id = delta['stock_id']
            if not stock_id in self.historical_book_data:
                sio.emit('historical-book', {'stockId':stock_id})
                return
            elif self.historical_book_data[stock_id]['to_tx'] != delta['from_tx']:
                sio.emit('open-book', {'stock_id':stock_id})

            stock_data = self.historical_book_data[stock_id]
            patch(stock_data['data'], delta['delta_data'])
            stock_data['to_tx'] = delta['to_tx']
            sio.emit(
                'historical-book',
                {stock_id:stock_data['data']}
            )

        
        @sio.on('candles')
        def candles_handler(data):
            stock_id = data['stock_id']
            self.candles_data.update({stock_id:data})

            result = {stock_id:self.candles_data[stock_id].copy()}
            if '1' in result[stock_id]:
                result[stock_id].update({'buy':result[stock_id]['1']})
                del result[stock_id]['1']
            if '2' in result[stock_id]:
                result[stock_id].update({'sell':result[stock_id]['2']})
                del result[stock_id]['2']
            sio.emit('candles', result)
        

        @sio.on('candles-delta')
        def candles_delta_handler(delta):
            stock_id = delta['stock_id']
            if not stock_id in self.candles_data:
                sio.emit('candles', {'stockId':stock_id})
                return
            elif self.candles_data[stock_id]['to_tx'] != delta['from_tx']:
                sio.emit('open-book', {'stock_id':stock_id})

            stock_data = self.candles_data[stock_id]
            patch(stock_data['data'], delta['delta_data'])
            stock_data['to_tx'] = delta['to_tx']

            result = {stock_id:stock_data.copy()}
            if '1' in result[stock_id]:
                result[stock_id].update({'buy':result[stock_id]['1']})
                del result[stock_id]['1']
            if '2' in result[stock_id]:
                result[stock_id].update({'sell':result[stock_id]['2']})
                del result[stock_id]['2']
            sio.emit('candles', result)

        @sio.on('board')
        def board_handler(data):
            self.board_data = data
            sio.emit('board', data)
        
        @sio.on('board-delta')
        def board_delta_handler(delta):
            if self.board_data['to_tx'] != delta['from_tx']:
                sio.emit('board')
                return
            patch(self.board_data['data'], delta['delta_data'])
            self.board_data['to_tx'] = delta['to_tx']
            sio.emit('ticker', self.board_data['data'])

        self.sio = sio
        

    def subscribe(self, *market_pairs):
        for pair in market_pairs:
            self.sio.emit('subscribe', pair)
        
    def unsubscribe(self, *market_pairs):
        for pair in market_pairs:
            self.sio.emit('unsubscribe', pair)
        
    def on(self, event, handler):
        self.sio.on(event, handler)