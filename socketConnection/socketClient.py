import socketio 
from cryptomarket.exchange.client import Client

class Socket:
    """This class starts a socket connection to interact with cryptomarket.
    """
    def __init__(self,keysFile):
        #Here your keys are loaded
        keysAsFile = open(keysFile,"r")
        keys = keysAsFile.readline().split(",")

        #create the api client from sdk
        client = Client(keys[0],keys[1])

        #get uid and socid
        sockids = client.get_auth_socket()

        #start socket connection
        sio = socketio.Client()

        @sio.event
        def connect():
            print("I'm connected!")

        @sio.event
        def connect_error():
            print("The connection failed!")

        @sio.event
        def disconnect():
            print("I'm disconnected!")
        
        sio.connect("wss://worker.cryptomkt.com:443")

        #sending keys for authentication
        #sio.emit("user-auth")

    """def emit(self,data):
        sio.emit("data")"""
