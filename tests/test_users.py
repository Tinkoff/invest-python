# pylint: disable=redefined-outer-name,unused-variable

from unittest import mock

import pytest

from tinkoff.invest.services import OldUsersService


@pytest.fixture()
def users_service():
    return mock.create_autospec(spec=OldUsersService)


def test_get_accounts(users_service):
    _ = users_service.get_accounts()

    users_service.get_accounts.assert_called_once()


def test_get_margin_attributes(users_service):
    _ = users_service.get_margin_attributes(
        account_id=mock.Mock(),
    )

    users_service.get_margin_attributes.assert_called_once()


def test_get_user_tariff(users_service):
    _ = users_service.get_user_tariff()

    users_service.get_user_tariff.assert_called_once()


def test_get_info(users_service):
    _ = users_service.get_info()

    users_service.get_info.assert_called_once()
