from typing import List, Tuple

from .constants import APP_NAME


def get_metadata(token: str) -> List[Tuple[str, str]]:
    return [("authorization", f"Bearer {token}"), ("x-app-name", APP_NAME)]
