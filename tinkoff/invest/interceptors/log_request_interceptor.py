from grpc.framework.foundation.callable_util import Outcome

from tinkoff.invest.interceptors import generic_interceptor
from tinkoff.invest.interceptors.client_call_details import ClientCallDetails
from tinkoff.invest.logging import get_tracking_id_from_call, log_request


def log_request_interceptor():
    def intercept_call(
        call_details: ClientCallDetails,
        request_iterator,
        request_streaming,
        response_streaming,
    ):
        def postprocess(call: Outcome):
            log_request(get_tracking_id_from_call(call), call_details.method)
            return call

        return call_details, request_iterator, postprocess

    return generic_interceptor.create(intercept_call)
