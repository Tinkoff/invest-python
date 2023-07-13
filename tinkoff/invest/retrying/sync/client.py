from tinkoff.invest import Client
from tinkoff.invest.retrying.settings_protocol import RetryClientSettingsProtocol
from tinkoff.invest.retrying.sync.grpc_interceptor import RetryClientInterceptor
from tinkoff.invest.retrying.sync.retry_manager import RetryManager


class RetryingClient(Client):
    def __init__(
        self,
        token: str,
        settings: RetryClientSettingsProtocol,
        **kwargs,
    ):
        self._retry_manager = RetryManager(settings=settings)
        self._retry_interceptor = RetryClientInterceptor(
            retry_manager=self._retry_manager
        )
        interceptors = kwargs.get("interceptors", [])
        interceptors.append(self._retry_interceptor)
        kwargs["interceptors"] = interceptors
        super().__init__(token, **kwargs)
