import dataclasses
from decimal import Decimal

from tinkoff.invest import CandleInterval
from tinkoff.invest.typedefs import ShareId


@dataclasses.dataclass
class StrategySettings:
    share_id: ShareId
    max_transaction_price: Decimal
    candle_interval: CandleInterval
