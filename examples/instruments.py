import os

from tinkoff.invest import Client
from tinkoff.invest.grpc.instruments_pb2 import FindInstrumentRequest

TOKEN = os.environ["INVEST_TOKEN"]
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


def main():
    with Client(TOKEN) as client:
        r = client.instruments.FindInstrument(FindInstrumentRequest(query="тинькофф"))
        for i in r.instruments:
            print(i.name)


if __name__ == "__main__":
    main()
