import logging
import time
from typing import Any

from tinkoff.invest.logging import get_metadata_from_call
from tinkoff.invest.retrying.base_retry_manager import BaseRetryManager

logger = logging.getLogger(__name__)


class RetryManager(BaseRetryManager):
    def call_with_retries(self, call: Any):
        retries_left = self.get_initial_retries()
        while retries_left > 0:
            logger.debug("Trying to call")
            result = call()
            logger.debug("Call succeeded")
            exception = result.exception()
            if not exception:
                return result
            retries_left -= 1
            logger.debug("Retries left = %s", retries_left)
            metadata = get_metadata_from_call(exception)
            seconds_to_sleep = self.extract_seconds_to_sleep(metadata)
            self._sleep(seconds_to_sleep)

        logger.debug("RetryManager exhausted, no retries left")
        return result

    def _sleep(self, seconds_to_sleep):
        time.sleep(seconds_to_sleep)
