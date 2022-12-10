from tinkoff.invest.interceptors import generic_interceptor
from tinkoff.invest.interceptors.client_call_details import ClientCallDetails
from tinkoff.invest.logging import get_tracking_id_from_call, log_request


def logging_interceptor():
    def intercept_call(
        call_details: ClientCallDetails,
        request_iterator,
        request_streaming,
        response_streaming,
    ):
        log_request(get_tracking_id_from_call(call), call_details.method)
        call_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            call_details.metadata,
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )
        return call_details, request_iterator, None

    return generic_interceptor.create(intercept_call)
