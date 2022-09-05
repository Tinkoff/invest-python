import grpc

from tinkoff.invest.retrying.aio.retry_manager import AsyncRetryManager


class AsyncRetryClientInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(
        self, retry_manager: AsyncRetryManager
    ):  # pylint: disable=super-init-not-called
        self._retry_manager = retry_manager

    async def _intercept_with_retry(self, continuation, client_call_details, request):
        async def call():
            return await continuation(client_call_details, request)

        return await self._retry_manager.call_with_retries(call=call)

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        return await self._intercept_with_retry(
            continuation, client_call_details, request
        )
