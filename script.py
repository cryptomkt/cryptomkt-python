import cryptomarket.exchange.client as c
import cryptomarket.exchange.socket as s

client = c.Client("2755964/01BgCj1WCabUw2", "JeufSrS1FoYxD/AOEpRF0XMrwVFFU1OL80qViE94R80Tpz9VZ0Cr5Rl8EXhmX0Yd3HcD89T6S")

auth = client.get_auth_socket()

s.Socket(auth)