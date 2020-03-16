from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging 

import socketio

from pubsub import pub

from .patch_json import patch

class Socket(object):
    def __init__(self, socketids, debug=False):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        f_handler = logging.FileHandler('socket.log')
        if debug:
            f_handler.setLevel(logging.DEBUG)
        f_format = logging.Formatter('%(asctime)s - %(message)s')
        #f_format.datefmt = '%d-%b-%y %H:%M:%S'
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)
        self.logger = logger

        self.url_worker = 'https://worker.cryptomkt.com'
        self.currencies_data = dict()
        self.balance_data = dict()
        self.open_orders_data = dict()
        self.historical_orders_data = dict()
        self.operated_data = dict()
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

        self.logger.debug('connecting to cryptomarket')
        sio.connect(self.url_worker)

        self.logger.debug('authenticating')
        sio.emit('user-auth', socketids)


        @sio.on('currencies')
        def currencies_handler(data):
            self.logger.debug('currencies recieved: {}'.format(data))
            self.currencies_data = data
        
        @sio.on('currencies-delta')
        def currencies_delta_handler(delta):
            self.logger.debug('delta-currencies recieved: {}'.format(delta))
            if self.currencies_data['to_tx'] != delta['from_tx']:
                sio.emit('currencies')
                return

            patch(self.currencies_data['data'], delta['delta_data'])
            self.currencies_data['to_tx'] = delta['to_tx']
        

        @sio.on('balance')
        def balance_handler(data):
            self.logger.debug('balance recieved: {}'.format(data))
            for _, value in data['data'].items():
                currency = value['currency']
                currency_data = self.currencies_data['data'][currency]
                value.update({
                    'currency_kind':currency_data['kind'],
                    'currency_name':currency_data['name'],
                    'currency_big_name':currency_data['big_name'],
                    'currency_prefix':currency_data['prefix'],
                    'currency_postfix':currency_data['postfix'],
                    'currency_decimals':currency_data['decimals'],
                })
            self.balance_data = data

            pub.sendMessage(
                'balance', 
                data=self.balance_data['data'].copy())
        
        
        @sio.on('balance-delta')
        def balance_delta_handler(deltas):
            self.logger.debug('balance-delta recieved: {}'.format(deltas))
            for delta in deltas:
                if self.balance_data['to_tx'] != delta['from_tx']:
                    sio.emit('balance')
                    return

                patch(self.balance_data['data'], delta['delta_data'])
                self.balance_data['to_tx'] = delta['to_tx']
        
            for _, value in self.balance_data['data'].items():
                currency = value['currency']
                currency_data = self.currencies_data['data'][currency]
                value.update({
                    'currency_kind':currency_data['kind'],
                    'currency_name':currency_data['name'],
                    'currency_big_name':currency_data['big_name'],
                    'currency_prefix':currency_data['prefix'],
                    'currency_postfix':currency_data['postfix'],
                    'currency_decimals':currency_data['decimals'],
                })

            pub.sendMessage(
                'balance', 
                data=self.balance_data['data'].copy())

        @sio.on('open-orders')
        def open_orders_handler(data):
            self.logger.debug('open-orders recieved: {}'.format(data))
            self.open_orders_data = data
            pub.sendMessage('open-orders', data=data['data'].copy())
        
        @sio.on('open-orders-delta')
        def open_orders_delta_handler(deltas):
            self.logger.debug('open-orders-delta recieved: {}'.format(deltas))
            for delta in deltas:
                if self.open_orders_data['to_tx'] != delta['from_tx']:
                    sio.emit('open-orders')
                    return 

                patch(self.open_orders_data['data'], delta['delta_data'])
                self.open_orders_data['to_tx'] = delta['to_tx']

            pub.sendMessage(
                'open-orders', 
                data=self.open_orders_data['data'].copy())


        @sio.on('historical-orders')
        def historical_orders_handler(data):
            self.logger.debug('historical-orders recieved: {}'.format(data))
            self.historical_orders_data = data
            pub.sendMessage('historical-orders', data=data['data'].copy())
        
        @sio.on('historical-orders-delta')
        def historical_orders_delta_handler(deltas):
            self.logger.debug('historical-orders-delta recieved: {}'.format(deltas))
            for delta in deltas:
                if self.historical_orders_data['to_tx'] != delta['from_tx']:
                    sio.emit('historical-orders')
                    return

                patch(self.historical_orders_data['data'], delta['delta_data'])
                self.historical_orders_data['to_tx'] = delta['to_tx']
        
            pub.sendMessage(
                'historical-orders', 
                data=self.historical_orders_data['data'].copy())


        @sio.on('operated')
        def operated_handler(data):
            self.logger.debug('operated recieved: {}'.format(data))
            self.operated_data = data
            pub.sendMessage('operated', data=data['data'].copy())
        
        @sio.on('operated-delta')
        def operated_delta_handler(deltas):
            self.logger.debug('operated-delta recieved: {}'.format(deltas))
            for delta in deltas:
                if self.operated_data['to_tx'] != delta['from_tx']:
                    sio.emit('operated')
                    return

                patch(self.operated_data['data'], delta['delta_data'])
                self.operated_data['to_tx'] = delta['to_tx']

            pub.sendMessage(
                'operated', 
                data=self.operated_data['data'].copy())


        @sio.on('open-book')
        def open_book_handler(data):
            self.logger.debug('open-book recieved: {}'.format(data))
            stock_id = data['stock_id']
            self.open_book_data.update({stock_id:data})
            pub.sendMessage(
                'open-book', 
                data={
                    stock_id:{
                        'buy':data['data']['1'],
                        'sell':data['data']['2']}
                }.copy()
            )
        
        @sio.on('open-book-delta')
        def open_book_delta_handler(delta):
            self.logger.debug('open-book-delta recieved: {}'.format(delta))
            stock_id = delta['stock_id']
            if (stock_id not in self.open_book_data
                or self.open_book_data[stock_id]['to_tx'] != delta['from_tx']):
                sio.emit('open-book', {'stockId':stock_id})
                return

            stock_data = self.open_book_data[stock_id]
            patch(stock_data['data'], delta['delta_data'])
            stock_data['to_tx'] = delta['to_tx']

            pub.sendMessage(
                'open-book', 
                data={
                    stock_id:{
                        'buy':stock_data['data']['1'],
                        'sell':stock_data['data']['2']}
                }.copy()
            )


        @sio.on('historical-book')
        def historical_book_handler(data):
            self.logger.debug('historical-book recieved: {}'.format(data))
            stock_id = data['stock_id']
            self.historical_book_data.update({stock_id:data})
            pub.sendMessage(
                'historical-book',
                data={stock_id:data['data']}.copy()
            )
        
        @sio.on('historical-book-delta')
        def historical_book_delta_handler(delta):
            self.logger.debug('historical-book-delta recieved: {}'.format(delta))
            stock_id = delta['stock_id']
            if (stock_id not in self.historical_book_data
               or self.historical_book_data[stock_id]['to_tx'] != delta['from_tx']):
                sio.emit('historical-book', {'stock_id':stock_id})
                return

            stock_data = self.historical_book_data[stock_id]
            patch(stock_data['data'], delta['delta_data'])
            stock_data['to_tx'] = delta['to_tx']

            pub.sendMessage(
                'historical-book',
                data={stock_id:stock_data['data']}.copy()
            )

        
        @sio.on('candles')
        def candles_handler(data):
            self.logger.debug('candles recieved: {}'.format(data))
            stock_id = data['stock_id']
            self.candles_data.update({stock_id:data})

            result = {stock_id:self.candles_data[stock_id]}.copy()
            if '1' in result[stock_id]:
                result[stock_id].update({'buy':result[stock_id]['1']})
                del result[stock_id]['1']
            if '2' in result[stock_id]:
                result[stock_id].update({'sell':result[stock_id]['2']})
                del result[stock_id]['2']
            pub.sendMessage('candles', data=result)
        

        @sio.on('candles-delta')
        def candles_delta_handler(delta):
            self.logger.debug('candles-delta recieved: {}'.format(delta))
            stock_id = delta['stock_id']
            if (stock_id not in self.candles_data
                or self.candles_data[stock_id]['to_tx'] != delta['from_tx']):
                sio.emit('candles', {'stock_id':stock_id})
                return

            stock_data = self.candles_data[stock_id]
            patch(stock_data['data'], delta['delta_data'])
            stock_data['to_tx'] = delta['to_tx']

            result = {stock_id:stock_data}.copy()
            if '1' in result[stock_id]:
                result[stock_id].update({'buy':result[stock_id]['1']})
                del result[stock_id]['1']
            if '2' in result[stock_id]:
                result[stock_id].update({'sell':result[stock_id]['2']})
                del result[stock_id]['2']
            pub.sendMessage('candles', data=result)

        @sio.on('board')
        def board_handler(data):
            self.logger.debug('board recieved: {}'.format(data))
            self.board_data = data
            pub.sendMessage('ticker', data=data.copy())
        
        @sio.on('board-delta')
        def board_delta_handler(delta):
            self.logger.debug('board-delta recieved: {}'.format(delta))
            if self.board_data['to_tx'] != delta['from_tx']:
                sio.emit('board')
                return

            patch(self.board_data['data'], delta['delta_data'])
            self.board_data['to_tx'] = delta['to_tx']
            pub.sendMessage('ticker', data=self.board_data['data'].copy())

        self.sio = sio

    def subscribe(self, *market_pairs):
        self.logger.debug('starting subscriptions: {}'.format(market_pairs))
        for pair in market_pairs:
            self.sio.emit('subscribe', pair)
        
    def unsubscribe(self, *market_pairs):
        self.logger.debug('ending subscriptions: {}'.format(market_pairs))
        for pair in market_pairs:
            self.sio.emit('unsubscribe', pair)

    def on(self, event, handler):
        self.logger.debug('subscribing to event: {}'.format(event))
        pub.subscribe(handler, event)
