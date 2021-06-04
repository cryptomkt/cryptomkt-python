import json
import logging
from threading import Thread

import websocket


class WebsocketManager:
    def __init__(self, handler, uri):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(logging.DEBUG)
        self.uri = uri
        self.connected = False

        def on_message(ws, message):
            msg = json.loads(message)
            try:
                handler.handle(msg)
            except Exception as e:
                handler.on_error(e)
                self.close()

        def on_error(ws, error):
            self._log.error("websocket error: "+ error)
            handler.on_error(error)


        def on_close(ws):
            self._log.debug('websocket connection closed')
            handler.on_close()

        def on_open(ws):
            self._log.debug(f'websocket connection open at: {ws.url}')
            self.connected = True
            handler._on_open()
            
        self.ws = websocket.WebSocketApp(
            self.uri,
            on_message = on_message,
            on_error = on_error,
            on_close = on_close,
            on_open= on_open,
        )

        self.thread = Thread(target=self.ws.run_forever)

    def connect(self):
        self.thread.start()

    def send(self, msg):
        if not self.thread.is_alive():
            raise ConnectionError('websocket connection is not active')
        msg_as_str = json.dumps(msg)
        self.ws.send(msg_as_str)

    def close(self):
        try:
            self.ws.close()
        except Exception as e:
            self._log.error("unable to close socket: " + str(e))
        self.connected = False
        self.thread.join(5)
            
