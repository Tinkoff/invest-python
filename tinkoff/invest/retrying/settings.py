import dataclasses

from tinkoff.invest.retrying.settings_protocol import RetryClientSettingsProtocol


@dataclasses.dataclass()
class RetryClientSettings(RetryClientSettingsProtocol):
    use_retry: bool = True
    max_retry_attempt: int = 3
