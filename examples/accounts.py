import os

import grpc

from tinkoff.invest.constants import INVEST_GRPC_API
from tinkoff.invest.grpc import users_pb2, users_pb2_grpc

TOKEN = os.environ["INVEST_TOKEN"]


def run():
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(INVEST_GRPC_API, creds)
    with channel:
        stub = users_pb2_grpc.UsersServiceStub(channel)
        metadata = [("authorization", f"Bearer {TOKEN}")]
        response = stub.GetAccounts(
            request=users_pb2.GetAccountsRequest(), metadata=metadata
        )
        print("Response ", response)  # noqa:T001


run()
