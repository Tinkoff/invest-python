from grpc.framework.foundation.callable_util import Outcome

from tinkoff.invest.logging import get_tracking_id_from_call, log_request

from . import generic_interceptor
from .client_call_details import ClientCallDetails


def log_request_interceptor():
    def intercept_call(
        call_details: ClientCallDetails,
        request_iterator,
        _request_streaming,
        _response_streaming,
    ):
        def postprocess(call: Outcome):
            log_request(get_tracking_id_from_call(call), call_details.method)
            return call

        return call_details, request_iterator, postprocess

    return generic_interceptor.create(intercept_call)
