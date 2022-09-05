from tinkoff.invest import AsyncClient
from tinkoff.invest.retrying.aio.grpc_interceptor import AsyncRetryClientInterceptor
from tinkoff.invest.retrying.aio.retry_manager import AsyncRetryManager
from tinkoff.invest.retrying.settings import RetryClientSettings


class AsyncRetryingClient(AsyncClient):
    def __init__(
        self,
        token: str,
        settings: RetryClientSettings,
        **kwargs,
    ):
        self._retry_manager = AsyncRetryManager(settings=settings)
        self._retry_interceptor = AsyncRetryClientInterceptor(
            retry_manager=self._retry_manager
        )
        interceptors = kwargs.get("interceptors", [])
        interceptors.append(self._retry_interceptor)
        kwargs["interceptors"] = interceptors
        super().__init__(token, **kwargs)
