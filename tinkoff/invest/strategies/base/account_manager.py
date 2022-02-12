import logging
from decimal import Decimal

from tinkoff.invest import Quotation
from tinkoff.invest.services import Services
from tinkoff.invest.strategies.base.errors import (
    InsufficientMarginalTradeFunds,
    MarginalTradeIsNotActive,
)
from tinkoff.invest.strategies.base.strategy_settings_base import StrategySettings
from tinkoff.invest.utils import quotation_to_decimal

logger = logging.getLogger(__name__)


class AccountManager:
    def __init__(self, services: Services, strategy_settings: StrategySettings):
        self._services = services
        self._strategy_settings = strategy_settings

    def get_current_balance(self) -> Decimal:
        account_id = self._strategy_settings.account_id
        portfolio_response = self._services.operations.get_portfolio(
            account_id=account_id
        )
        balance = portfolio_response.total_amount_currencies
        return quotation_to_decimal(Quotation(units=balance.units, nano=balance.nano))

    def ensure_marginal_trade(self) -> None:
        account_id = self._strategy_settings.account_id
        try:
            response = self._services.users.get_margin_attributes(account_id=account_id)
        except Exception as e:
            raise MarginalTradeIsNotActive() from e
        value = quotation_to_decimal(response.funds_sufficiency_level)
        if value <= 1:
            raise InsufficientMarginalTradeFunds()
        logger.info("Marginal trade is active")
