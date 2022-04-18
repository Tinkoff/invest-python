import os

from tinkoff.invest import Client

CONTRACT_PREFIX = "tinkoff.public.invest.api.contract.v1."


TOKEN = os.environ["INVEST_TOKEN"]


def main() -> None:
    with Client(TOKEN) as client:
        accounts = client.users.get_accounts()
        print("\nСписок текущих аккаунтов\n")
        for account in accounts.accounts:
            print("\t", account.id, account.name, account.access_level.name)

        print("\nТекущие лимиты\n")
        tariff = client.users.get_user_tariff()
        for unary_limit in tariff.unary_limits:
            methods = [m.replace(CONTRACT_PREFIX, "") for m in unary_limit.methods]
            print(unary_limit.limit_per_minute, "запросов в минуту для:")
            print("\t" + "\n\t".join(methods))

        for stream_limit in tariff.stream_limits:
            print(stream_limit.limit, "коннект(а/ов) для:")
            streams = [s.replace(CONTRACT_PREFIX, "") for s in stream_limit.streams]
            print("\t" + "\n\t".join(streams))

        print("\nИнформация\n")
        info = client.users.get_info()
        print(info)


if __name__ == "__main__":
    main()
