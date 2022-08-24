from pydantic import BaseSettings, conint


class RetryClientSettings(BaseSettings):
    use_retry: bool = True
    max_retry_attempt: conint(ge=0) = 3
