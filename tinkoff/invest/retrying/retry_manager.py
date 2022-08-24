import logging
import time
from typing import Any

from tinkoff.invest.logging import Metadata, get_metadata_from_call
from tinkoff.invest.retrying.settings import RetryClientSettings

logger = logging.getLogger(__name__)


class RetryManager:
    def __init__(self, settings: RetryClientSettings):
        self._settings = settings

    def call_with_retries(self, call: Any):
        retries_left = self._settings.max_retry_attempt
        if not self._settings.use_retry:
            retries_left = 0
            logger.debug("Retrying disabled")
        retries_left += 1
        while retries_left > 0:
            logger.debug("Trying to call")
            result = call()
            logger.debug("Call succeeded")
            exception = result.exception()
            if not exception:
                return result
            retries_left -= 1
            logger.debug("Retries left = %s", retries_left)
            self._sleep(exception)

        logger.debug("RetryManager exhausted, no retries left")
        return result

    def _sleep(self, exception):
        metadata: Metadata = get_metadata_from_call(exception)
        logger.debug("Received metadata %s", metadata)
        seconds_to_sleep = metadata.ratelimit_reset
        logger.debug("Sleeping for %s seconds", seconds_to_sleep)
        time.sleep(seconds_to_sleep)
