import os
import sys

import grpc

from tinkoff.invest.constants import INVEST_GRPC_API
from tinkoff.invest.grpc import users_pb2, users_pb2_grpc


def main() -> int:
    try:
        token = os.environ["INVEST_TOKEN"]
    except KeyError:
        print("env INVEST_TOKEN not found")  # noqa:T001
        return 1
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(INVEST_GRPC_API, creds)
    with channel:
        stub = users_pb2_grpc.UsersServiceStub(channel)
        metadata = [("authorization", f"Bearer {token}")]
        response = stub.GetAccounts(
            request=users_pb2.GetAccountsRequest(), metadata=metadata
        )
        print("Response ", response)  # noqa:T001
    return 0


if __name__ == "__main__":
    sys.exit(main())
