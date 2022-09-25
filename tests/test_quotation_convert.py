from decimal import Decimal
from random import randrange

import pytest

from tinkoff.invest import Quotation
from tinkoff.invest.utils import decimal_to_quotation, quotation_to_decimal

MAX_UNITS = 999_999_999_999
MAX_NANO = 999_999_999


@pytest.fixture()
def quotation(request) -> Quotation:
    raw = request.param
    return Quotation(units=raw["units"], nano=raw["nano"])


class TestQuotationArithmetic:
    @pytest.mark.parametrize(
        ("quotation", "decimal"),
        [
            ({"units": 114, "nano": 250000000}, Decimal("114.25")),
            ({"units": -200, "nano": -200000000}, Decimal("-200.20")),
            ({"units": -0, "nano": -10000000}, Decimal("-0.01")),
        ],
        indirect=["quotation"],
    )
    def test_quotation_to_decimal(self, quotation: Quotation, decimal: Decimal):
        actual = quotation_to_decimal(quotation)

        assert actual == decimal

    @pytest.mark.parametrize(
        ("quotation", "decimal"),
        [
            ({"units": 114, "nano": 250000000}, Decimal("114.25")),
            ({"units": -200, "nano": -200000000}, Decimal("-200.20")),
            ({"units": -0, "nano": -10000000}, Decimal("-0.01")),
        ],
        indirect=["quotation"],
    )
    def test_decimal_to_quotation(self, decimal: Decimal, quotation: Quotation):
        actual = decimal_to_quotation(decimal)

        assert actual.units == quotation.units
        assert actual.nano == quotation.nano

    @pytest.mark.parametrize(
        ("quotation_left", "quotation_right"),
        [
            (
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
            ),
            (
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
                Quotation(units=0, nano=0),
            ),
            (
                Quotation(units=0, nano=0),
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
            ),
            (
                Quotation(units=-0, nano=-200000000),
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
            ),
            (
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
                Quotation(units=-0, nano=-200000000),
            ),
        ],
    )
    @pytest.mark.parametrize(
        "operation",
        [
            lambda x, y: x - y,
            lambda x, y: x + y,
        ],
    )
    def test_operations(
        self, quotation_left: Quotation, quotation_right: Quotation, operation
    ):
        decimal_left = quotation_to_decimal(quotation_left)
        decimal_right = quotation_to_decimal(quotation_right)

        quotation = operation(quotation_left, quotation_right)

        expected_decimal = operation(decimal_left, decimal_right)
        actual_decimal = quotation_to_decimal(quotation)
        assert actual_decimal == expected_decimal

    @pytest.mark.parametrize(
        ("quotation_left", "quotation_right"),
        [
            (
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
            ),
            (
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
                Quotation(units=0, nano=0),
            ),
            (
                Quotation(units=0, nano=0),
                Quotation(
                    units=randrange(-MAX_UNITS, MAX_UNITS),
                    nano=randrange(-MAX_NANO, MAX_NANO),
                ),
            ),
            (
                Quotation(units=0, nano=0),
                Quotation(units=0, nano=0),
            ),
            (
                Quotation(units=-10, nano=0),
                Quotation(units=10, nano=0),
            ),
            (
                Quotation(units=0, nano=-200000000),
                Quotation(units=0, nano=-200000000),
            ),
        ],
    )
    @pytest.mark.parametrize(
        "comparator",
        [
            lambda x, y: x > y,
            lambda x, y: x >= y,
            lambda x, y: x < y,
            lambda x, y: x <= y,
            lambda x, y: x == y,
            lambda x, y: x != y,
            lambda y, x: x > y,
            lambda y, x: x >= y,
            lambda y, x: x < y,
            lambda y, x: x <= y,
            lambda y, x: x == y,
            lambda y, x: x != y,
        ],
    )
    def test_comparison(
        self, quotation_left: Quotation, quotation_right: Quotation, comparator
    ):
        decimal_left = quotation_to_decimal(quotation_left)
        decimal_right = quotation_to_decimal(quotation_right)

        actual_comparison = comparator(quotation_left, quotation_right)

        expected_comparison = comparator(decimal_left, decimal_right)
        assert actual_comparison == expected_comparison
