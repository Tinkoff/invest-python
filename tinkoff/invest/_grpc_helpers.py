# pylint:disable=no-name-in-module
import dataclasses
import enum
from abc import ABC
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import (
    Any,
    Optional,
    Tuple,
    Type,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

from google.protobuf import symbol_database  # noqa:I900
from google.protobuf.timestamp_pb2 import Timestamp  # noqa:I90

_sym_db = symbol_database.Default()

T = TypeVar("T")


def ts_to_datetime(value: Timestamp) -> datetime:
    ts = value.seconds + (value.nanos / 1e9)
    return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=ts)


def datetime_to_ts(value: datetime) -> Tuple[int, int]:
    seconds = int(value.timestamp())
    nanos = int(value.microsecond * 1e3)
    return seconds, nanos


# Proto 3 data types
TYPE_ENUM = "enum"
TYPE_BOOL = "bool"
TYPE_INT32 = "int32"
TYPE_INT64 = "int64"
TYPE_UINT32 = "uint32"
TYPE_UINT64 = "uint64"
TYPE_SINT32 = "sint32"
TYPE_SINT64 = "sint64"
TYPE_FLOAT = "float"
TYPE_DOUBLE = "double"
TYPE_FIXED32 = "fixed32"
TYPE_SFIXED32 = "sfixed32"
TYPE_FIXED64 = "fixed64"
TYPE_SFIXED64 = "sfixed64"
TYPE_STRING = "string"
TYPE_BYTES = "bytes"
TYPE_MESSAGE = "message"
TYPE_MAP = "map"

PLACEHOLDER: Any = object()


@dataclasses.dataclass(frozen=True)
class FieldMetadata:
    """Stores internal metadata used for parsing & serialization."""

    # Protobuf field number
    number: int
    # Protobuf type name
    proto_type: str
    # Map information if the proto_type is a map
    map_types: Optional[Tuple[str, str]] = None
    # Groups several "one-of" fields together
    group: Optional[str] = None
    # Describes the wrapped type (e.g. when using google.protobuf.BoolValue)
    wraps: Optional[str] = None
    # Is the field optional
    optional: Optional[bool] = False

    @staticmethod
    def get(field: dataclasses.Field) -> "FieldMetadata":
        """Returns the field metadata for a dataclass field."""
        return field.metadata["proto"]


def dataclass_field(
    number: int,
    proto_type: str,
    *,
    map_types: Optional[Tuple[str, str]] = None,
    group: Optional[str] = None,
    wraps: Optional[str] = None,
    optional: bool = False,
) -> dataclasses.Field:
    """Creates a dataclass field with attached protobuf metadata."""
    return dataclasses.field(
        default=None if optional else PLACEHOLDER,  # type:ignore # noqa:IF100
        metadata={
            "proto": FieldMetadata(
                number, proto_type, map_types, group, wraps, optional
            )
        },
    )


def enum_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, TYPE_ENUM, group=group, optional=optional)


def bool_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, TYPE_BOOL, group=group, optional=optional)


def int32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_INT32, group=group, optional=optional)


def int64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_INT64, group=group, optional=optional)


def uint32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_UINT32, group=group, optional=optional)


def uint64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_UINT64, group=group, optional=optional)


def sint32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_SINT32, group=group, optional=optional)


def sint64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_SINT64, group=group, optional=optional)


def float_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_FLOAT, group=group, optional=optional)


def double_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_DOUBLE, group=group, optional=optional)


def fixed32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_FIXED32, group=group, optional=optional)


def fixed64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_FIXED64, group=group, optional=optional)


def sfixed32_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_SFIXED32, group=group, optional=optional)


def sfixed64_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_SFIXED64, group=group, optional=optional)


def string_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_STRING, group=group, optional=optional)


def bytes_field(
    number: int, group: Optional[str] = None, optional: bool = False
) -> Any:
    return dataclass_field(number, TYPE_BYTES, group=group, optional=optional)


def message_field(
    number: int,
    group: Optional[str] = None,
    wraps: Optional[str] = None,
    optional: bool = False,
) -> Any:
    return dataclass_field(
        number, TYPE_MESSAGE, group=group, wraps=wraps, optional=optional
    )


def map_field(
    number: int, key_type: str, value_type: str, group: Optional[str] = None
) -> Any:
    return dataclass_field(
        number, TYPE_MAP, map_types=(key_type, value_type), group=group
    )


class Enum(enum.IntEnum):
    @classmethod
    def from_string(cls, name: str) -> "Enum":
        try:
            return cls._member_map_[name]  # type: ignore  # pylint:disable=no-member
        except KeyError as e:
            raise ValueError(f"Unknown value {name} for enum {cls.__name__}") from e


class Message(ABC):
    ...


class Service(ABC):
    _stub_factory: Any

    def __init__(self, channel, metadata):
        self.stub = self._stub_factory(channel)
        self.metadata = metadata


_UNKNOWN: Any = object()
PRIMITIVE_TYPES = (str, float, bool, int)


class UnknownType(TypeError):
    pass


# pylint:disable=too-many-nested-blocks
# pylint:disable=too-many-branches
# pylint:disable=too-many-locals
# pylint:disable=too-many-nested-blocks
# pylint:disable=too-many-statements
def protobuf_to_dataclass(pb_obj: Any, dataclass_type: Type[T]) -> T:  # noqa:C901
    dataclass_hints = get_type_hints(dataclass_type)
    dataclass_obj = dataclass_type()
    dataclass_fields = dataclass_type.__dataclass_fields__  # type:ignore
    for field_name, field_type in dataclass_hints.items():
        pb_value = getattr(pb_obj, field_name)
        field_value = _UNKNOWN
        oneof = dataclass_fields[field_name].metadata["proto"].group
        if oneof and pb_obj.WhichOneof(oneof) != field_name:
            setattr(dataclass_obj, field_name, None)
            continue

        origin = get_origin(field_type)
        if origin is None:
            if field_type in PRIMITIVE_TYPES:
                field_value = pb_value
            if field_type == Decimal:
                field_value = Decimal(str(pb_value))
            elif issubclass(field_type, datetime):
                field_value = ts_to_datetime(pb_value)
            elif dataclasses.is_dataclass(field_type):
                field_value = protobuf_to_dataclass(pb_value, field_type)
            elif issubclass(field_type, Enum):
                field_value = field_type(pb_value)
        elif origin == list:
            args = get_args(field_type)
            first_arg = args[0]
            if first_arg in PRIMITIVE_TYPES:
                field_value = pb_value
            elif dataclasses.is_dataclass(first_arg):
                field_value = [
                    protobuf_to_dataclass(item, first_arg) for item in pb_value
                ]
            elif first_arg == Decimal:
                field_value = [Decimal(str(item)) for item in pb_value]
            elif first_arg == datetime:
                field_value = [ts_to_datetime(item) for item in pb_value]
            elif issubclass(field_type, Enum):
                field_value = [field_type(item) for item in pb_value]

        if field_value is _UNKNOWN:
            raise UnknownType(f'type "{field_type}" unknown')
        setattr(dataclass_obj, field_name, field_value)

    return dataclass_obj


def dataclass_to_protobuff(dataclass_obj: Any, protobuff_obj: T) -> T:  # noqa:C901
    dataclass_type = type(dataclass_obj)
    dataclass_hints = get_type_hints(dataclass_type)
    for field_name, field_type in dataclass_hints.items():
        field_value = getattr(dataclass_obj, field_name)
        if field_value is PLACEHOLDER:
            continue
        origin = get_origin(field_type)
        if origin is None:
            if field_type in PRIMITIVE_TYPES:
                setattr(protobuff_obj, field_name, field_value)
            elif issubclass(field_type, datetime):
                field_name_ = field_name
                if field_name == "from_":
                    field_name_ = "from"
                pb_value = getattr(protobuff_obj, field_name_)
                seconds, nanos = datetime_to_ts(field_value)
                pb_value.seconds = seconds
                pb_value.nanos = nanos
            elif dataclasses.is_dataclass(field_type):
                pb_value = getattr(protobuff_obj, field_name)
                dataclass_to_protobuff(field_value, pb_value)
            elif issubclass(field_type, Enum):
                if isinstance(field_value, int):
                    field_value = field_type(field_value)
                setattr(protobuff_obj, field_name, field_value.value)
            else:
                raise UnknownType(f"type {field_type} unknown")
        elif origin == list:
            args = get_args(field_type)
            first_arg = args[0]
            pb_value = getattr(protobuff_obj, field_name)
            if first_arg in PRIMITIVE_TYPES:
                pb_value.extend(item for item in field_value)
            elif dataclasses.is_dataclass(first_arg):
                descriptor = protobuff_obj.DESCRIPTOR  # type:ignore
                field_descriptor = descriptor.fields_by_name[field_name].message_type
                type_ = _sym_db.GetPrototype(field_descriptor)
                pb_value.extend(
                    dataclass_to_protobuff(item, type_()) for item in field_value
                )
            elif issubclass(first_arg, Enum):
                pb_value.extend(item.value for item in field_value)
            else:
                raise UnknownType(f"type {field_type} unknown")
        else:
            raise UnknownType(f"type {field_type} unknown")

    return protobuff_obj
