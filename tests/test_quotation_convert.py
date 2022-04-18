from decimal import Decimal

import pytest

from tinkoff.invest import Quotation
from tinkoff.invest.utils import decimal_to_quotation, quotation_to_decimal


@pytest.fixture()
def quotation(request) -> Quotation:
    raw = request.param
    return Quotation(units=raw["units"], nano=raw["nano"])


@pytest.mark.parametrize(
    ("quotation", "decimal"),
    [
        ({"units": 114, "nano": 250000000}, Decimal("114.25")),
        ({"units": -200, "nano": -200000000}, Decimal("-200.20")),
        ({"units": -0, "nano": -10000000}, Decimal("-0.01")),
    ],
    indirect=["quotation"],
)
def test_quotation_to_decimal(quotation: Quotation, decimal: Decimal):
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
def test_decimal_to_quotation(decimal: Decimal, quotation: Quotation):
    actual = decimal_to_quotation(decimal)

    assert actual.units == quotation.units
    assert actual.nano == quotation.nano
