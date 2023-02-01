from typing import Iterable, Tuple

from tinkoff.invest.interceptors.header_adder_interceptor import (
    header_adder_interceptor,
)


def metadata_adder_interceptor(metadata: Iterable[Tuple[str, str]]):
    return header_adder_interceptor(metadata)
