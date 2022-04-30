import csv
import dataclasses
import itertools
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, Iterable, Iterator, Optional, Tuple

import dateutil.parser  # noqa: I900  'dateutil' not listed as a requirement

from tinkoff.invest.caching.cache_settings import (
    MarketDataCacheSettings,
    meta_file_context,
)
from tinkoff.invest.caching.instrument_date_range_market_data import (
    InstrumentDateRangeData,
)
from tinkoff.invest.caching.interface import IInstrumentMarketDataStorage
from tinkoff.invest.schemas import CandleInterval, HistoricCandle
from tinkoff.invest.utils import dataclass_from_dict, datetime_range_floor

logger = logging.getLogger(__name__)


class InstrumentMarketDataStorage(
    IInstrumentMarketDataStorage[Iterable[InstrumentDateRangeData]]
):
    def __init__(
        self, figi: str, interval: CandleInterval, settings: MarketDataCacheSettings
    ):
        self._figi = figi
        self._interval = interval
        self._settings = settings
        self._settings.base_cache_dir.mkdir(parents=True, exist_ok=True)
        self._meta_path = self._get_metafile(
            file=self._get_base_file_path(figi=self._figi, interval=self._interval)
        )

    def _get_base_file_path(self, figi: str, interval: CandleInterval) -> Path:
        instrument_dir = self._get_cache_dir_for_instrument(figi=figi)
        instrument_dir.mkdir(parents=True, exist_ok=True)
        return self._get_cache_file_for_instrument(
            instrument_dir=instrument_dir, interval=interval
        )

    def _get_file_path(self, date_range: Tuple[datetime, datetime]) -> Path:
        start, end = date_range
        start.strftime("%s")
        filepath = self._get_base_file_path(figi=self._figi, interval=self._interval)
        filepath = filepath.parent / (
            filepath.name + f'-{start.strftime("%s")}-{end.strftime("%s")}'
        )
        return filepath.with_suffix(f".{self._settings.format_extension}")

    def _get_metafile(self, file: Path) -> Path:
        return file.with_suffix(f".{self._settings.meta_extension}")

    def _get_cache_file_for_instrument(
        self, instrument_dir: Path, interval: CandleInterval
    ) -> Path:
        return instrument_dir / interval.name

    def _get_cache_dir_for_instrument(self, figi: str) -> Path:
        return self._settings.base_cache_dir / figi

    def _get_range_from_file(
        self, reader: Iterable[Dict], request_range: Tuple[datetime, datetime]
    ) -> Iterable[Dict]:
        start, end = request_range
        for row in reader:

            row_time = dateutil.parser.parse(row["time"])
            if start <= row_time <= end:
                yield row
            if end < row_time:
                return

    def _get_candles_from_cache(
        self,
        file: Path,
        request_range: Tuple[datetime, datetime],
    ) -> Generator[HistoricCandle, None, None]:
        with open(file, "r") as infile:  # pylint: disable=W1514
            reader = csv.DictReader(infile, fieldnames=self._settings.field_names)
            reader_iter = iter(reader)
            next(reader_iter)  # pylint: disable=R1708
            for row in self._get_range_from_file(
                reader_iter, request_range=request_range
            ):
                yield self._candle_from_row(row)

    def _order_rows(
        self, dict_reader1: Iterator[Dict], dict_reader2: Iterator[Dict]
    ) -> Iterable[Dict]:
        dict_reader_iter1 = iter(dict_reader1)
        dict_reader_iter2 = iter(dict_reader2)

        while True:
            try:
                candle_dict1 = next(dict_reader_iter1)
            except StopIteration:
                yield from dict_reader_iter2
                break
            try:
                candle_dict2 = next(dict_reader_iter2)
            except StopIteration:
                yield from dict_reader_iter1
                break

            candle_dict_time1 = dateutil.parser.parse(candle_dict1["time"])
            candle_dict_time2 = dateutil.parser.parse(candle_dict2["time"])
            if candle_dict_time1 > candle_dict_time2:
                dict_reader_iter1 = itertools.chain([candle_dict1], dict_reader_iter1)
                yield candle_dict2
            elif candle_dict_time1 < candle_dict_time2:
                dict_reader_iter2 = itertools.chain([candle_dict2], dict_reader_iter2)
                yield candle_dict1
            else:
                yield candle_dict1

    def _order_candles(
        self,
        tmp_dict_reader: Iterator[Dict],
        historic_candles: Iterable[HistoricCandle],
    ) -> Iterable[Dict]:
        tmp_iter = iter(tmp_dict_reader)
        candle_iter = iter(historic_candles)

        while True:
            try:
                tmp_candle_dict = next(tmp_iter)
            except StopIteration:
                yield from [dataclasses.asdict(candle) for candle in candle_iter]
                break
            try:
                candle = next(candle_iter)
            except StopIteration:
                yield from tmp_iter
                break

            tmp_candle_time = dateutil.parser.parse(tmp_candle_dict["time"])
            if tmp_candle_time > candle.time:
                tmp_iter = itertools.chain([tmp_candle_dict], tmp_iter)
                yield dataclasses.asdict(candle)
            elif tmp_candle_time < candle.time:
                candle_iter = itertools.chain([candle], candle_iter)
                yield tmp_candle_dict
            else:
                yield tmp_candle_dict

    def _write_candles_file(self, data: InstrumentDateRangeData) -> Path:
        file = self._get_file_path(date_range=data.date_range)
        with open(file, mode="w") as csv_file:  # pylint: disable=W1514
            writer = csv.DictWriter(csv_file, fieldnames=self._settings.field_names)
            writer.writeheader()
            for candle in data.historic_candles:
                writer.writerow(dataclasses.asdict(candle))
        return file

    def _candle_from_row(self, row: Dict[str, str]) -> HistoricCandle:
        return dataclass_from_dict(HistoricCandle, row)

    def _get_intersection(
        self,
        request_range: Tuple[datetime, datetime],
        cached_range: Tuple[datetime, datetime],
    ) -> Optional[Tuple[datetime, datetime]]:
        request_start, request_end = request_range
        cached_start, cached_end = cached_range
        max_start = max(request_start, cached_start)
        min_end = min(request_end, cached_end)
        if max_start <= min_end:
            return max_start, min_end
        return None

    def _merge_intersecting_files(  # pylint: disable=R0914
        self,
        file1: Path,
        range1: Tuple[datetime, datetime],
        file2: Path,
        range2: Tuple[datetime, datetime],
    ) -> Tuple[Tuple[datetime, datetime], Path]:
        new_range = (min(min(range1), min(range2)), max(max(range1), max(range2)))
        new_file = self._get_file_path(date_range=new_range)
        assert file1 != file2
        assert file2 != new_file
        assert file1 != new_file

        with open(file1, "r") as infile1:  # pylint: disable=W1514
            reader1 = csv.DictReader(infile1, fieldnames=self._settings.field_names)
            reader_iter1 = iter(reader1)
            next(reader_iter1)  # skip header

            with open(file2, "r") as infile2:  # pylint: disable=W1514
                reader2 = csv.DictReader(infile2, fieldnames=self._settings.field_names)
                reader_iter2 = iter(reader2)
                next(reader_iter2)  # skip header

                with open(new_file, mode="w") as csv_file:  # pylint: disable=W1514
                    writer = csv.DictWriter(
                        csv_file, fieldnames=self._settings.field_names
                    )
                    writer.writeheader()

                    for candle_dict in self._order_rows(
                        dict_reader1=reader_iter1, dict_reader2=reader_iter2
                    ):
                        writer.writerow(candle_dict)

                    file1.unlink()
                    file2.unlink()
        return new_range, new_file

    def _get_distinct_product(self, cached_range_in_file) -> Iterable[Tuple]:
        for i, items1 in enumerate(  # pylint: disable=R1702
            cached_range_in_file.items()
        ):
            for j, items2 in enumerate(cached_range_in_file.items()):
                if i < j:
                    yield items1, items2

    def _try_merge_files(
        self, cached_range_in_file: Dict[Tuple[datetime, datetime], Path]
    ) -> Dict[Tuple[datetime, datetime], Path]:
        new_cached_range_in_file = cached_range_in_file.copy()
        file_pairs = self._get_distinct_product(new_cached_range_in_file)
        for (cached_range, cached_file), (cached_range2, cached_file2) in file_pairs:
            intersection_range = self._get_intersection(
                request_range=cached_range2, cached_range=cached_range
            )
            if intersection_range is not None:
                merged_range, merged_file = self._merge_intersecting_files(
                    file1=cached_file,
                    range1=cached_range,
                    file2=cached_file2,
                    range2=cached_range2,
                )
                new_cached_range_in_file[merged_range] = merged_file
                del new_cached_range_in_file[cached_range]
                del new_cached_range_in_file[cached_range2]
                return self._try_merge_files(new_cached_range_in_file)
        return new_cached_range_in_file

    def get(
        self, request_range: Tuple[datetime, datetime]
    ) -> Iterable[InstrumentDateRangeData]:
        request_range = datetime_range_floor(request_range)
        with meta_file_context(meta_file_path=self._meta_path) as meta_file:
            cached_range_in_file = meta_file.cached_range_in_file

        for cached_range, cached_file in cached_range_in_file.items():
            intersection = self._get_intersection(
                request_range=request_range, cached_range=cached_range
            )
            if intersection is not None:
                candles = self._get_candles_from_cache(
                    cached_file, request_range=request_range
                )
                yield InstrumentDateRangeData(
                    date_range=intersection, historic_candles=candles
                )

    def update(self, data_list: Iterable[InstrumentDateRangeData]):
        with meta_file_context(meta_file_path=self._meta_path) as meta_file:
            for data in data_list:
                data.date_range = datetime_range_floor(data.date_range)
                new_file = self._write_candles_file(data)
                assert data.date_range not in meta_file.cached_range_in_file
                meta_file.cached_range_in_file[data.date_range] = new_file
            new_cached_range_in_file = self._try_merge_files(
                meta_file.cached_range_in_file
            )
            meta_file.cached_range_in_file = new_cached_range_in_file
