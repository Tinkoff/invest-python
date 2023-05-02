import os

from tinkoff.invest import Client

TOKEN = os.environ["INVEST_TOKEN"]


def main():
    with Client(TOKEN) as client:
        r = client.instruments.get_brands()
        for brand in r.brands:
            print(brand)


if __name__ == "__main__":
    main()
