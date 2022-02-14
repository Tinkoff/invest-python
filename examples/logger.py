import logging

from tinkoff.invest import Client, RequestError
from tinkoff.invest.env_tools.token import TOKEN

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    with Client(TOKEN) as client:
        _ = client.users.get_accounts().accounts
        try:
            client.users.get_margin_attributes(account_id="123")
        except RequestError as err:
            tracking_id = err.metadata.tracking_id if err.metadata else ""
            logger.error("Error tracking_id=%s code=%s", tracking_id, str(err.code))


if __name__ == "__main__":
    main()
