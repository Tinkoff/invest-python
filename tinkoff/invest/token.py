import os
import warnings

warnings.warn(
    'Token module is deprecated. Use `TOKEN = os.environ["INVEST_TOKEN"]` instead',
    DeprecationWarning,
)


class InvestTokenNotFound(Exception):
    pass


try:
    TOKEN = os.environ["INVEST_TOKEN"]
except KeyError as e:
    raise InvestTokenNotFound("env INVEST_TOKEN not found") from e
