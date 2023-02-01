import collections
from typing import Iterable, Tuple

import grpc

from . import generic_interceptor
from .client_call_details import ClientCallDetails


class _ClientCallDetails(
    collections.namedtuple(
        "_ClientCallDetails", ("method", "timeout", "metadata", "credentials")
    ),
    grpc.ClientCallDetails,
):
    pass


def header_adder_interceptor(headers: Iterable[Tuple[str, str]]):
    def intercept_call(
        call_details: ClientCallDetails,
        request_iterator,
        _request_streaming,
        _response_streaming,
    ):
        metadata = []
        if call_details.metadata is not None:
            metadata = list(call_details.metadata)
        metadata_headers = [header for header, value in metadata]

        for header, value in headers:
            if header in metadata_headers:
                continue
            metadata_headers.append(header)
            metadata.append(
                (
                    header,
                    value,
                )
            )
        call_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            metadata,
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )
        return call_details, request_iterator, None

    return generic_interceptor.create(intercept_call)
