import logging
import os

from tinkoff.invest import Client

TOKEN = os.environ["INVEST_TOKEN"]

logging.basicConfig(level=logging.INFO)


def main():
    with Client(TOKEN) as client:
        print(client.users.get_accounts())


if __name__ == "__main__":
    main()
