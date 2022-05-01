import contextlib
import dataclasses
import enum
import pickle  # noqa: S403 Consider possible security implications.
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, Sequence, Tuple

from definitions import PACKAGE_DIR  # noqa: I900


class MarketDataCacheFormat(str, enum.Enum):
    CSV = "csv"


@dataclasses.dataclass()
class MarketDataCacheSettings:
    base_cache_dir: Path = PACKAGE_DIR / ".market_data_cache"
    use_cache: bool = True
    format_extension: MarketDataCacheFormat = MarketDataCacheFormat.CSV
    field_names: Sequence[str] = (
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "is_complete",
    )
    meta_extension: str = "meta"


@dataclasses.dataclass()
class FileMetaData:
    cached_range_in_file: Dict[Tuple[datetime, datetime], Path]


@contextlib.contextmanager
def meta_file_context(meta_file_path: Path) -> Generator[FileMetaData, None, None]:
    try:
        with open(meta_file_path, "rb") as f:
            meta = pickle.load(f)  # noqa: S301
    except FileNotFoundError:
        meta = FileMetaData(cached_range_in_file={})
    try:
        yield meta
    finally:
        with open(meta_file_path, "wb") as f:
            pickle.dump(meta, f)
