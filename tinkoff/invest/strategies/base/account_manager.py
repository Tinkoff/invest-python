from decimal import Decimal

from tinkoff.invest.services import Services


class AccountManager:
    def __init__(self, services: Services):
        self._services = services

    def get_current_balance(self) -> Decimal:
        raise NotImplementedError()
