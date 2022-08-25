import os
from tinkoff.invest import Client, GetOperationsByCursorRequest


token = os.environ['INVEST_TOKEN']


with Client(token) as client:
    accounts = client.users.get_accounts()
    account_id = accounts.accounts[0].id

    def get_request(cursor=''):
        return GetOperationsByCursorRequest(
            account_id=account_id,
            instrument_id="BBG004730N88",
            cursor=cursor,
            limit=1,
        )

    operations = client.operations.get_operations_by_cursor(get_request())
    print(operations)
    while operations.has_next:
        request = get_request(cursor=operations.next_cursor)
        operations = client.operations.get_operations_by_cursor(request)
        print(operations)
