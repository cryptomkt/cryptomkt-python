import socketio as s
import exchange.client as c
#getting api keys
keysFile = open("keys.txt", "r")

keys = keysFile.readline().split(",")

client = c.Client(keys[0], keys[1])

print(client)

sockeys = client.get_account()

sio = s.Client()

sio.connect("wss://worker.cryptomkt.com:443")

"""@sio.event
def message(data):
    print()"""