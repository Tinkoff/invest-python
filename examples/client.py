import os
import sys

from tinkoff.invest import Client


def main() -> int:
    try:
        token = os.environ["INVEST_TOKEN"]
    except KeyError:
        print("env INVEST_TOKEN not found")  # noqa:T001
        return 1
    with Client(token) as client:
        print(client.users.get_accounts())  # noqa:T001
        print(client.instruments.bonds(instrument_status=1))  # noqa:T001

    return 0


if __name__ == "__main__":
    sys.exit(main())
