from typing import List, Optional, Tuple

from .constants import APP_NAME


def get_metadata(token: str, app_name: Optional[str] = None) -> List[Tuple[str, str]]:
    if not app_name:
        app_name = APP_NAME

    return [("authorization", f"Bearer {token}"), ("x-app-name", app_name)]
