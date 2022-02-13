from tinkoff.invest import Client
from tinkoff.invest.env_tools.token import TOKEN


def main():
    with Client(TOKEN) as client:
        print(client.users.get_accounts())


if __name__ == "__main__":
    main()
