import os

from tinkoff.invest.typedefs import AccountId


class InvestAccountNotFound(Exception):
    pass


try:
    ACCOUNT_ID = AccountId(os.environ["INVEST_ACCOUNT_ID"])
except KeyError as e:
    raise InvestAccountNotFound("env INVEST_ACCOUNT_ID not found") from e
