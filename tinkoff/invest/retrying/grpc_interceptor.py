import grpc

from tinkoff.invest.retrying.retry_manager import RetryManager


class RetryClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, retry_manager: RetryManager):
        self._retry_manager = retry_manager

    def _intercept_with_retry(self, continuation, client_call_details, request):
        def call():
            return continuation(client_call_details, request)

        return self._retry_manager.call_with_retries(call=call)

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return self._intercept_with_retry(continuation, client_call_details, request)
