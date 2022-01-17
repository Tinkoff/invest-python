# pylint: disable=redefined-outer-name,unused-variable

from unittest import mock

import pytest

from tinkoff.invest.services import UsersService


@pytest.fixture()
def users_service():
    return mock.create_autospec(spec=UsersService)


def test_get_accounts(users_service):
    response = users_service.get_accounts()  # noqa: F841
    users_service.get_accounts.assert_called_once()


def test_get_margin_attributes(users_service):
    response = users_service.get_margin_attributes(  # noqa: F841
        account_id=mock.Mock(),
    )
    users_service.get_margin_attributes.assert_called_once()


def test_get_user_tariff(users_service):
    response = users_service.get_user_tariff()  # noqa: F841
    users_service.get_user_tariff.assert_called_once()


def test_get_info(users_service):
    response = users_service.get_info()  # noqa: F841
    users_service.get_info.assert_called_once()
