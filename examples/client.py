import sys

from tinkoff.invest import Client
from tinkoff.invest.token import TOKEN


def main() -> int:
    with Client(TOKEN) as client:
        print(client.users.get_accounts())

    return 0


if __name__ == "__main__":
    sys.exit(main())
