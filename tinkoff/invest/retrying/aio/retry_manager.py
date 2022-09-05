import asyncio
import logging
from typing import Any

from grpc.aio import AioRpcError

from tinkoff.invest.logging import get_metadata_from_aio_error
from tinkoff.invest.retrying.base_retry_manager import BaseRetryManager

logger = logging.getLogger(__name__)


class AsyncRetryManager(BaseRetryManager):
    async def call_with_retries(self, call: Any):
        retries_left = self.get_initial_retries()
        while retries_left > 0:
            logger.debug("Trying to call")
            response = await call()
            try:
                await response
                logger.debug("Call succeeded")
                return response
            except AioRpcError as exception:
                retries_left -= 1
                logger.debug("Retries left = %s", retries_left)

                metadata = get_metadata_from_aio_error(exception)
                seconds_to_sleep = self.extract_seconds_to_sleep(metadata)
                await self._sleep(seconds_to_sleep)

        logger.debug("RetryManager exhausted, no retries left")
        return response

    async def _sleep(self, seconds_to_sleep):
        await asyncio.sleep(seconds_to_sleep)
