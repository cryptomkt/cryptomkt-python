from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import socketio
import time

from .client import Client


class Socket(object):
    def __init__(self, socketids):

        self.socketids = socketids
        sio =  socketio.Client()

        @sio.event
        def connect():
            print('connection established')

        @sio.event
        def my_message(data):
            print('message received with ', data)
            sio.emit('my response', {'response': 'my response'})

        @sio.event
        def disconnect():
            print('disconnected from server')

        sio.connect('https://worker.cryptomkt.com')
        sio.emit('socket-auth', socketids)

        @sio.on('currencies')
        def currencies_handler(msg):
            print('currencies received')
            print(msg)
    
        def board_handler(msg):
            print('board received')
            print(msg)
            return msg
        sio.on('board-delta', board_handler)

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