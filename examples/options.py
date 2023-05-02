import os

from tinkoff.invest import Client

TOKEN = os.environ["INVEST_TOKEN"]


def main():
    with Client(TOKEN) as client:
        r = client.instruments.options()
        for instrument in r.instruments:
            print(instrument)


if __name__ == "__main__":
    main()
