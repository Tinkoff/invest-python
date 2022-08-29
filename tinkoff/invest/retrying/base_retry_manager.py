import logging

from tinkoff.invest.retrying.settings import RetryClientSettings

logger = logging.getLogger(__name__)


class BaseRetryManager:
    def __init__(self, settings: RetryClientSettings):
        self._settings = settings

    def get_initial_retries(self):
        retries_left = self._settings.max_retry_attempt
        if not self._settings.use_retry:
            retries_left = 0
            logger.debug("Retrying disabled")
        retries_left += 1
        return retries_left

    @staticmethod
    def extract_seconds_to_sleep(metadata) -> int:
        logger.debug("Received metadata %s", metadata)
        seconds_to_sleep = metadata.ratelimit_reset
        logger.debug("Sleeping for %s seconds", seconds_to_sleep)
        return seconds_to_sleep
