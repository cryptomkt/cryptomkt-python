from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import socketio
import time
import logging

debugging = True

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename='socket.log',
    format='%(asctime)s [%(levelname)s] %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p')

if debuging:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


from .client import Client

class Socket(object):
    def __init__(self, socketids):
        self.url_worker = 'https://worker.cryptomkt.com'
        self.currencies_data = None
        self.balances_data = None
        self.operated_data = None
        self.open_orders_data = None
        self.historical_orders_data = None
        self.open_book_data = None
        self.historical_book_data = None
        self.candles_data = None
        self.board_data = None

        self.socketids = socketids
        sio =  socketio.Client()

        @sio.event
        def connect():
            logger.info('connecting socket')

        @sio.event
        def my_message(data):
            print('message received with ', data)
            sio.emit('my response', {'response': 'my response'})

        @sio.event
        def disconnect():
            print('disconnected from server')

        sio.connect(self.url_worker)

        logger.info('authenticating socket')
        sio.emit('socket-auth', socketids)


        @sio.on('currencies')
        def currencies_handler(data):
            log.info('currencies received')
            print(type(msg))
    

        @sio.on('open-orders')
        def open_orders_handler(msg):
            print('open-orders received')
            print(msg)

        @sio.on('ticker')
        def ticker_handler(msg):
            print('ticker received')
            print(msg)

        # sio.wait()
        self.sio = sio