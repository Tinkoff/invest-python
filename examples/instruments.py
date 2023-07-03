import os

from tinkoff.invest import Client

TOKEN = os.environ["INVEST_TOKEN"]


def main():
    with Client(TOKEN) as client:
        r = client.instruments.find_instrument(query="BBG001M2SC01")
        for i in r.instruments:
            print(i)


if __name__ == "__main__":
    main()
