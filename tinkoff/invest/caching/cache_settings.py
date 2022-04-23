import contextlib
import dataclasses
import enum
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, Sequence, Tuple

from definitions import PACKAGE_DIR


class MarketDataCacheFormat(str, enum.Enum):
    CSV = ".csv"


@dataclasses.dataclass()
class MarketDataCacheSettings:
    base_cache_dir: Path = PACKAGE_DIR / ".market_data_cache"
    use_cache: bool = True
    format: MarketDataCacheFormat = MarketDataCacheFormat.CSV
    field_names: Sequence[str] = (
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "is_complete",
    )
    meta_suffix: str = ".meta"


@dataclasses.dataclass()
class FileMetaData:
    cached_range_in_file: Dict[Tuple[datetime, datetime], Path]


@contextlib.contextmanager
def meta_file_context(meta_file_path: Path) -> Generator[FileMetaData, None, None]:
    try:
        with open(meta_file_path, "rb") as f:
            meta = pickle.load(f)
    except FileNotFoundError:
        meta = FileMetaData(cached_range_in_file={})
    try:
        yield meta
    except Exception as e:
        raise e
    finally:
        with open(meta_file_path, "wb") as f:
            pickle.dump(meta, f)
