from abc import ABC, abstractmethod
from aiomarine.fields.limits import SQLInt, SQLBigInt
from typing import Any, Optional


class BaseDataType(ABC):
    """
    This class describes a base data type.
    """

    def __init__(
        self,
        primary_key: Optional[bool] = False,
        unique: Optional[bool] = False,
        null: Optional[bool] = True,
        default: Optional[Any] = None,
    ):
        self.primary_key: bool = primary_key
        self.unique: bool = unique
        self.null: bool = null
        self.default: Any = default

    @abstractmethod
    def validate(self, value: Any) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def to_db_value(self, value: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def from_db_value(self, value: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def to_sql_type(self) -> str:
        raise NotImplementedError()


class IntegerField(BaseDataType):
    """
    This class describes an integer field.
    """

    __slots__ = (
        'max_value',
        'min_value',
        'primary_key',
        'unique',
        'null',
        'default'
    )

    def __init__(
        self,
        max_value: Optional[int] = SQLInt.SIGNED_MIN,
        min_value: Optional[int] = SQLInt.SIGNED_MAX,
        primary_key: Optional[bool] = False,
        unique: Optional[bool] = False,
        null: Optional[bool] = True,
        default: Optional[int] = None,
    ):
        self.min_value = min_value
        self.max_value = max_value

        super().__init__(primary_key=primary_key, unique=unique, null=null, default=default)

    def validate(self, value: Any) -> bool:
        if self.primary_key and value is None:
            return True
        if value is None and self.null:
            return True
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False

        return True

    def to_db_value(self, value: Any) -> int:
        if self.primary_key and value is None:
            return 0

        return int(value) if value is not None else self.default

    def from_db_value(self, value: Any) -> int:
        return int(value) if value is not None else None

    def to_sql_type(self) -> str:
        return "INTEGER"


class BigIntegerField(IntegerField):
    __slots__ = (
        'max_value',
        'min_value',
        'primary_key',
        'unique',
        'null',
        'default'
    )

    def __init__(
        self,
        max_value: Optional[int] = SQLBigInt.SIGNED_MAX,
        min_value: Optional[int] = SQLBigInt.SIGNED_MIN,
        primary_key: Optional[bool] = False,
        unique: Optional[bool] = False,
        null: Optional[bool] = True,
        default: Optional[int] = None,
    ):
        super().__init__(max_value=max_value, min_value=min_value, primary_key=primary_key,
                         unique=unique, null=null, default=default)

    def to_sql_type(self) -> str:
        return "BIGINT"

