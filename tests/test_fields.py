from aiomarine.fields import BigIntegerField, IntegerField
from aiomarine.fields.limits import SQLBigInt, SQLInt


def test_limits():
    assert SQLInt.SIGNED_MIN == -2147483648
    assert SQLInt.SIGNED_MAX == 2147483647

    assert SQLBigInt.SIGNED_MIN == -9223372036854775808
    assert SQLBigInt.SIGNED_MAX == 9223372036854775807


def test_fields():
    integer = IntegerField()
    assert integer.to_sql_type() == 'INTEGER'

    biginteger = BigIntegerField()
    assert biginteger.to_sql_type() == 'BIGINT'
