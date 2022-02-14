import os

from tinkoff.invest.typedefs import ShareId


class InvestFigiNotFound(Exception):
    pass


try:
    FIGI = ShareId(os.environ["INVEST_FIGI"])
except KeyError as e:
    raise InvestFigiNotFound("env INVEST_FIGI not found") from e
