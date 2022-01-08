# pylint: disable=redefined-outer-name

import grpc
import grpc_testing
import pytest
from google.protobuf.timestamp_pb2 import Timestamp  # noqa: I900

from tinkoff.invest.grpc import users_pb2, users_pb2_grpc


@pytest.fixture()
def grpc_users_account():
    return users_pb2.Account(
        id="0",
        type=users_pb2.AccountType.ACCOUNT_TYPE_TINKOFF,
        name="Oleg",
        status=users_pb2.AccountStatus.ACCOUNT_STATUS_OPEN,
        opened_date=Timestamp(seconds=0),
        closed_date=Timestamp(seconds=100000000),
    )


@pytest.fixture()
def grpc_userserceservicer(grpc_users_account):
    class UsersService(users_pb2_grpc.UsersServiceServicer):
        def GetAccounts(self, request, context):
            return users_pb2.GetAccountsResponse(accounts=[grpc_users_account])

    return UsersService()


@pytest.fixture()
def grpc_server(grpc_userserceservicer):
    servicers = {
        users_pb2.DESCRIPTOR.services_by_name["UsersService"]: grpc_userserceservicer
    }

    return grpc_testing.server_from_dictionary(
        servicers, grpc_testing.strict_real_time()
    )


def test_getaccounts(grpc_server):
    request = users_pb2.GetAccountsRequest()

    getaccounts_method = grpc_server.invoke_unary_unary(
        method_descriptor=(
            users_pb2.DESCRIPTOR.services_by_name["UsersService"].methods_by_name[
                "GetAccounts"
            ]
        ),
        invocation_metadata={},
        request=request,
        timeout=1,
    )

    response, _, code, _ = getaccounts_method.termination()

    assert code == grpc.StatusCode.OK
    assert len(response.accounts) == 1
    response_sample_account = response.accounts[0]
    assert response_sample_account.id == "0"
    assert response_sample_account.name == "Oleg"
