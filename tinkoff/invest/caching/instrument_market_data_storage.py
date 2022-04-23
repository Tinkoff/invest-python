import contextlib
import csv
import dataclasses
import itertools
import pickle
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Iterable, Generator, Sequence, Any, Optional

import dateutil.parser

from tinkoff.invest import HistoricCandle, CandleInterval
from tinkoff.invest.caching.cache_settings import MarketDataCacheSettings, FileMetaData, \
    meta_file_context
from tinkoff.invest.caching.interface import IInstrumentMarketDataStorage
from tinkoff.invest.utils import dataclass_from_dict


@dataclasses.dataclass()
class InstrumentDateRangeData:
    date_range: Tuple[datetime, datetime]
    historic_candles: Sequence[HistoricCandle]


class CacheMissError(Exception):
    def __init__(self, cached_range: Tuple[datetime, datetime], request_range: Tuple[datetime, datetime]):
        self._cached_range = cached_range
        self._request_range = request_range

    def __str__(self):
        return f'Request range was [{self._request_range}], but cache range is [{self._cached_range}]'


class InstrumentMarketDataStorage(IInstrumentMarketDataStorage[Iterable[InstrumentDateRangeData]]):
    def __init__(self, figi: str, interval: CandleInterval, settings: MarketDataCacheSettings):
        self._figi = figi
        self._interval = interval
        self._settings = settings
        self._settings.base_cache_dir.mkdir(parents=True, exist_ok=True)
        self._meta_path = self._get_metafile(file=self._get_base_file_path(figi=self._figi, interval=self._interval))

    def _get_base_file_path(self, figi: str, interval: CandleInterval) -> Path:
        instrument_dir = self._get_cache_dir_for_instrument(figi=figi)
        instrument_dir.mkdir(parents=True, exist_ok=True)
        filepath = self._get_cache_file_for_instrument(instrument_dir=instrument_dir, interval=interval)
        return filepath.with_suffix(self._settings.format)

    def _get_file_path(self, range: Tuple[datetime, datetime]) -> Path:
        start, end = range
        start.strftime('%s')
        filepath = self._get_base_file_path(figi=self._figi, interval=self._interval)
        filepath = filepath.with_suffix(f'_[{start.strftime("%s")}-{end.strftime("%s")}]')
        return filepath.with_suffix(self._settings.format)

    def _get_metafile(self, file: Path) -> Path:
        return file.with_suffix(self._settings.meta_suffix)

    def _get_cache_file_for_instrument(self, instrument_dir: Path, interval: CandleInterval) -> Path:
        return instrument_dir / interval.name

    def _get_cache_dir_for_instrument(self, figi: str) -> Path:
        return self._settings.base_cache_dir / figi

    def _get_candles_from_cache(
        self,
        *,
        from_: datetime,
        to: datetime,
    ) -> Generator[HistoricCandle, None, None]:
        with open(self._file, "r") as infile:
            reader = csv.DictReader(infile, fieldnames=self._settings.field_names)
            for row in self._get_range(reader, from_, to):
                yield from self._candle_from_row(row)

    def _order_candles(self, tmp_dict_reader: Iterable[Dict], historic_candles: Iterable[HistoricCandle]) -> Iterable[Dict]:
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

            tmp_candle_time = dateutil.parser.parse(tmp_candle_dict['time'])
            if tmp_candle_time > candle.time:
                tmp_iter = itertools.chain([tmp_candle_dict], tmp_iter)
                yield dataclasses.asdict(candle)
            elif tmp_candle_time < candle.time:
                candle_iter = itertools.chain([candle], candle_iter)
                yield tmp_candle_dict
            else:
                yield tmp_candle_dict

    def _write_candles(self, historic_candles: Iterable[HistoricCandle]):

        with open(self._file, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self._settings.field_names)
            writer.writeheader()

            for candle_dict in self._order_candles(tmp_dict_reader=reader_iter, historic_candles=historic_candles):
                writer.writerow(candle_dict)


    def _write_candles(self, historic_candles: Iterable[HistoricCandle], file: Path):

        tmp_file = file.with_suffix('_tmp')
        with open(file, "r") as infile:
            reader = csv.reader(infile)
            with open(tmp_file, "w") as outfile:
                if file.exists():
                    writer = csv.writer(outfile)
                    for line in reader:
                        writer.writerow(line)
                else:
                    writer = csv.DictWriter(tmp_file, fieldnames=self._settings.field_names)
                    writer.writeheader()

        with open(tmp_file, "r") as infile:
            reader = csv.DictReader(infile, fieldnames=self._settings.field_names)
            reader_iter = iter(reader)
            next(reader_iter)  # skip header

            with open(file, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self._settings.field_names)
                writer.writeheader()

                for candle_dict in self._order_candles(tmp_dict_reader=reader_iter, historic_candles=historic_candles):
                    writer.writerow(candle_dict)

            tmp_file.unlink()


    def _candle_from_row(self, row: Dict[str, str]) -> HistoricCandle:
        return dataclass_from_dict(HistoricCandle, row)

    def _get_rows_by_index(self, reader: csv.DictReader, cached_index: Tuple[int, int]) -> Iterable[Dict[str, str]]:
        start_index, end_index = cached_index
        current_index = 0
        for row in reader:
            if start_index <= current_index <= end_index:
                yield row
            if current_index > end_index:
                return
            current_index += 1
        raise RuntimeError('Unreachable')

    def _filter_by_range(
        self, candles: Iterable[HistoricCandle], request_range: Tuple[datetime, datetime]
    ):
        request_start, request_end = request_range
        for candle in candles:
            if request_start <= candle.time <= request_end:
                yield candle

    def _is_request_in_cache(self, request_range: Tuple[datetime, datetime], cached_range: Tuple[datetime, datetime]):
        request_start, request_end = request_range
        cached_start, cached_end = cached_range
        return cached_start <= request_start and request_end <= cached_end

    def _get_intersection(self, request_range: Tuple[datetime, datetime], cached_range: Tuple[datetime, datetime]) -> Optional[Tuple[datetime, datetime]]:
        request_start, request_end = request_range
        cached_start, cached_end = cached_range
        max_start = max(request_start, cached_start)
        min_end = min(request_end, cached_end)
        if max_start <= min_end:
            return max_start, min_end
        else:
            return None

    def _load_by_index(self, cached_index: Tuple[int, int]) -> Iterable[HistoricCandle]:
        with open(self._file, "r") as infile:
            reader = csv.DictReader(infile, fieldnames=self._settings.field_names)
            for row in self._get_rows_by_index(reader, cached_index):
                yield self._candle_from_row(row)

    def _ensure_one_item(self, data: Iterable[Any]) -> Any:
        data = list(data)
        if len(data) > 1:
            raise NotImplementedError(
                'Multiple ranges caching is not currently supported'
            )
        item, = data
        return item

    def get(self, request_range: Tuple[datetime, datetime]) -> Iterable[InstrumentDateRangeData]:
        with meta_file_context(meta_file_path=self._meta_path) as meta_file:
            meta_file: FileMetaData = meta_file
            cached_ranges = meta_file.cached_ranges_to_idx.keys()
            cached_indexes = meta_file.cached_ranges_to_idx.values()
            cached_range = self._ensure_one_item(cached_ranges)
            cached_index, = cached_indexes
            if self._is_request_in_cache(request_range, cached_range):
                yield from self._filter_by_range(self._load_by_index(cached_index), request_range)
            else:
                raise CacheMissError(cached_range=cached_range, request_range=request_range)

    def _merge_into_file(self, cached_file: Path, cached_range: Tuple[datetime, datetime], data: InstrumentDateRangeData) -> Tuple[Tuple[datetime], Path]:
        start = min(min(data.date_range), min(cached_range))
        end = max(max(data.date_range), max(cached_range))
        new_file = self._get_file_path(range=(start, end))
        with open(cached_file, 'r') as cached:
            reader = csv.DictReader(cached, fieldnames=self._settings.field_names)
            for row in reader:
        with open(file, "r") as infile:
            reader = csv.reader(infile)
            with open(tmp_file, "w") as outfile:
                if file.exists():
                    writer = csv.writer(outfile)
                    for line in reader:
                        writer.writerow(line)
                else:
                    writer = csv.DictWriter(tmp_file,
                                            fieldnames=self._settings.field_names)
                    writer.writeheader()

        with open(tmp_file, "r") as infile:
            reader = csv.DictReader(infile,
                                    fieldnames=self._settings.field_names)
            reader_iter = iter(reader)
            next(reader_iter)  # skip header

            with open(file, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file,
                                        fieldnames=self._settings.field_names)
                writer.writeheader()

                for candle_dict in self._order_candles(
                        tmp_dict_reader=reader_iter,
                        historic_candles=historic_candles):
                    writer.writerow(candle_dict)

            tmp_file.unlink()

    def update(self, data_list: Iterable[InstrumentDateRangeData]):

        with meta_file_context(meta_file_path=self._meta_path) as meta_file:
            meta_file: FileMetaData = meta_file
            for data in data_list:
                new_cached_range_in_file = {}
                for cached_range, file in meta_file.cached_range_in_file.items():
                    intersection_range = self._get_intersection(request_range=data.date_range, cached_range=cached_range)
                    if intersection_range is not None:
                        merged_range, merged_file = self._merge_into_file(file, data)
                        new_cached_range_in_file[merged_range] = merged_file


            start = min(min(data.date_range), min(cached_range))
            end = max(max(data.date_range), max(cached_range))
