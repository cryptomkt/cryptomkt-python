from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import socketio


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

        @sio.event
        def disconnect():
            print('disconnected from server')

        sio.connect('https://worker.cryptomkt.com')
        
        sio.emit('socket-auth', socketids)

        @sio.on('board')
        def board_handler(msg):
            print(msg)

        self.sio = sio