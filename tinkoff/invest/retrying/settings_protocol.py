from typing import Protocol


class RetryClientSettingsProtocol(Protocol):
    use_retry: bool
    max_retry_attempt: int
