import logging
import sys

from tinkoff.invest import Client, RequestError
from tinkoff.invest.token import TOKEN

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> int:
    with Client(TOKEN) as client:
        _ = client.users.get_accounts().accounts
        try:
            client.users.get_margin_attributes(account_id="123")
        except RequestError as err:
            tracking_id = err.metadata.tracking_id if err.metadata else ""
            logger.error("Error tracking_id=%s code=%s", tracking_id, str(err.code))

    return 0


if __name__ == "__main__":
    sys.exit(main())
