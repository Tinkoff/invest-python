from tinkoff.invest import Client

TOKEN = ''

with Client(TOKEN) as client:
    print(client.users.get_accounts())