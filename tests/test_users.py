import unittest

import grpc
import grpc_testing
from google.protobuf.timestamp_pb2 import Timestamp  # noqa: I900

from tinkoff.invest.grpc import users_pb2, users_pb2_grpc


class UsersService(users_pb2_grpc.UsersServiceServicer):
    def GetAccounts(self, request, context):
        return users_pb2.GetAccountsResponse(
            accounts=[
                users_pb2.Account(
                    id="0",
                    type=users_pb2.AccountType.ACCOUNT_TYPE_TINKOFF,
                    name="Oleg",
                    status=users_pb2.AccountStatus.ACCOUNT_STATUS_OPEN,
                    opened_date=Timestamp(seconds=0),
                    closed_date=Timestamp(seconds=100000000),
                )
            ]
        )


class TestUserService(unittest.TestCase):
    def setUp(self):
        servicers = {
            users_pb2.DESCRIPTOR.services_by_name["UsersService"]: UsersService()
        }

        self.test_server = grpc_testing.server_from_dictionary(
            servicers, grpc_testing.strict_real_time()
        )

    def test_getaccounts(self):
        request = users_pb2.GetAccountsRequest()

        getaccounts_method = self.test_server.invoke_unary_unary(
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
