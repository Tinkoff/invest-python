from decimal import Decimal

from tinkoff.invest._grpc_helpers import Service


class AccountManager:
    def __init__(self, service: Service):
        self._service = service

    def get_current_balance(self) -> Decimal:
        raise NotImplementedError()
