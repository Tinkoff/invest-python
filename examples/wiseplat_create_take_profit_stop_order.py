"""Example - How to create takeprofit buy order."""
import logging
import os
from decimal import Decimal

from tinkoff.invest import (
    Client,
    InstrumentIdType,
    StopOrderDirection,
    StopOrderExpirationType,
    StopOrderType,
)
from tinkoff.invest.exceptions import InvestError
from tinkoff.invest.utils import decimal_to_quotation, quotation_to_decimal

TOKEN = os.environ["INVEST_TOKEN"]

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    """Example - How to create takeprofit buy order."""
    with Client(TOKEN) as client:
        response = client.users.get_accounts()
        account, *_ = response.accounts
        account_id = account.id
        logger.info("Orders: %s", client.orders.get_orders(account_id=account_id))

        figi = "BBG004730ZJ9"  # BBG004730ZJ9 - VTBR / BBG004730N88 - SBER

        # getting the last price for instrument
        last_price = client.market_data.get_last_prices(
            figi=[figi]).last_prices[0].price
        last_price = quotation_to_decimal(last_price)
        print(f'figi, last price = {last_price}')

        # setting the percentage by which the takeprofit stop order
        # should be set below the last price
        percent_down = 5

        # calculation of the price for takeprofit stop order
        calculated_price = last_price - last_price * Decimal(percent_down / 100)
        print(f'calculated_price = {calculated_price}')

        # getting the min price increment and the number of digits after point
        min_price_increment = client.instruments.get_instrument_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            id=figi).instrument.min_price_increment
        number_digits_after_point = 9 - len(str(min_price_increment.nano)) + 1
        min_price_increment = quotation_to_decimal(min_price_increment)
        print(f'min_price_increment = {min_price_increment}, '
              f'number_digits_after_point={number_digits_after_point}')

        # calculation of the price for instrument which is
        # divisible to min price increment
        calculated_price = round(
            calculated_price / min_price_increment) * min_price_increment
        print(f'let\'s send stop order at price = '
              f'{calculated_price:.{number_digits_after_point}f} divisible to '
              f'min price increment {min_price_increment}')

        # creating takeprofit buy order
        stop_order_type = StopOrderType.STOP_ORDER_TYPE_TAKE_PROFIT
        direction = StopOrderDirection.STOP_ORDER_DIRECTION_BUY
        exp_type = StopOrderExpirationType.STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL
        try:
            response = client.stop_orders.post_stop_order(
                figi=figi,
                quantity=1,
                price=decimal_to_quotation(Decimal(calculated_price)),
                stop_price=decimal_to_quotation(Decimal(calculated_price)),
                direction=direction,
                account_id=account_id,
                expiration_type=exp_type,
                stop_order_type=stop_order_type,
                expire_date=None,
            )
            print(response)
            print("stop_order_id=", response.stop_order_id)
        except InvestError as error:
            logger.error('Posting trade takeprofit order failed. Exception: %s', error)


if __name__ == "__main__":
    main()
