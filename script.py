import cryptomarket.exchange.client as c

client = c.Client("2755964/01BgCj1WCabUw2", "JeufSrS1FoYxD/AOEpRF0XMrwVFFU1OL80qViE94R80Tpz9VZ0Cr5Rl8EXhmX0Yd3HcD89T6S")

instant = client.get_instant('ETHCLP', 'buy', '100000')
print(instant)
