import os

from tinkoff.invest import Client

TOKEN = os.environ["INVEST_TOKEN"]


def main():
    with Client(TOKEN) as client:
        print(client.instruments.get_countries())


if __name__ == "__main__":
    main()
