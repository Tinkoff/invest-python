# pylint: disable=redefined-outer-name,unused-variable

from unittest import mock

import pytest

from tinkoff.invest.services import InstrumentsService


@pytest.fixture()
def instruments_service():
    return mock.MagicMock(spec=InstrumentsService)


def test_trading_schedules(instruments_service):
    response = instruments_service.trading_schedules(  # noqa: F841
        exchange=mock.Mock(),
        from_=mock.Mock(),
        to=mock.Mock(),
    )
    instruments_service.trading_schedules.assert_called_once()


def test_bond_by(instruments_service):
    response = instruments_service.bond_by(  # noqa: F841
        id_type=mock.Mock(),
        class_code=mock.Mock(),
        id=mock.Mock(),
    )
    instruments_service.bond_by.assert_called_once()


def test_bonds(instruments_service):
    response = instruments_service.bonds(  # noqa: F841
        instrument_status=mock.Mock(),
    )
    instruments_service.bonds.assert_called_once()


def test_currency_by(instruments_service):
    response = instruments_service.currency_by(  # noqa: F841
        id_type=mock.Mock(),
        class_code=mock.Mock(),
        id=mock.Mock(),
    )
    instruments_service.currency_by.assert_called_once()


def test_currencies(instruments_service):
    response = instruments_service.currencies(  # noqa: F841
        instrument_status=mock.Mock(),
    )
    instruments_service.currencies.assert_called_once()


def test_etf_by(instruments_service):
    response = instruments_service.etf_by(  # noqa: F841
        id_type=mock.Mock(),
        class_code=mock.Mock(),
        id=mock.Mock(),
    )
    instruments_service.etf_by.assert_called_once()


def test_etfs(instruments_service):
    response = instruments_service.etfs(  # noqa: F841
        instrument_status=mock.Mock(),
    )
    instruments_service.etfs.assert_called_once()


def test_future_by(instruments_service):
    response = instruments_service.future_by(  # noqa: F841
        id_type=mock.Mock(),
        class_code=mock.Mock(),
        id=mock.Mock(),
    )
    instruments_service.future_by.assert_called_once()


def test_futures(instruments_service):
    response = instruments_service.futures(  # noqa: F841
        instrument_status=mock.Mock(),
    )
    instruments_service.futures.assert_called_once()


def test_share_by(instruments_service):
    response = instruments_service.share_by(  # noqa: F841
        id_type=mock.Mock(),
        class_code=mock.Mock(),
        id=mock.Mock(),
    )
    instruments_service.share_by.assert_called_once()


def test_shares(instruments_service):
    response = instruments_service.shares(  # noqa: F841
        instrument_status=mock.Mock(),
    )
    instruments_service.shares.assert_called_once()


def test_get_accrued_interests(instruments_service):
    response = instruments_service.get_accrued_interests(  # noqa: F841
        figi=mock.Mock(),
        from_=mock.Mock(),
        to=mock.Mock(),
    )
    instruments_service.get_accrued_interests.assert_called_once()


def test_get_futures_margin(instruments_service):
    response = instruments_service.get_futures_margin(  # noqa: F841
        figi=mock.Mock(),
    )
    instruments_service.get_futures_margin.assert_called_once()


def test_get_instrument_by(instruments_service):
    response = instruments_service.get_instrument_by(  # noqa: F841
        id_type=mock.Mock(),
        class_code=mock.Mock(),
        id=mock.Mock(),
    )
    instruments_service.get_instrument_by.assert_called_once()


def test_get_dividends(instruments_service):
    response = instruments_service.get_dividends(  # noqa: F841
        figi=mock.Mock(),
        from_=mock.Mock(),
        to=mock.Mock(),
    )
    instruments_service.get_dividends.assert_called_once()
