import os

from tinkoff.invest.sandbox.client import SandboxClient

TOKEN = os.environ["INVEST_TOKEN"]


def main():
    with SandboxClient(TOKEN) as client:
        print(client.users.get_info())


if __name__ == "__main__":
    main()
