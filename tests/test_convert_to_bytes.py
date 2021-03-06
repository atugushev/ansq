from decimal import Decimal
from sys import version_info
from typing import Optional

import pytest

from ansq.utils import convert_to_bytes

PY37 = version_info >= (3, 7)


@pytest.mark.parametrize(
    'value, expected',
    (
        ('test_str', b'test_str'), (123, b'123'), (Decimal('3.14'), b'3.14'),
        (3.14159, b'3.14159'), (b'\xa1', b'\xa1'),
        ({'key': 'value', 123: 1337}, b'{"key":"value","123":1337}'),
        (
            'utf-16 str'.encode('utf-16'),
            b'\xff\xfeu\x00t\x00f\x00-\x001\x006\x00 \x00s\x00t\x00r\x00'
        ),
        (
            bytearray('This is real bytearray'.encode('utf-8')),
            b'This is real bytearray'
        ),
        (
            bytearray('hello'.encode('utf-32')),
            b'\xff\xfe\x00\x00h\x00\x00\x00e\x00\x00\x00l\x00'
            b'\x00\x00l\x00\x00\x00o\x00\x00\x00'
        ),
    )
)
def test_convert_to_bytes(value, expected):
    assert convert_to_bytes(value) == expected


if PY37:
    from dataclasses import dataclass

    @dataclass
    class Point:
        x: int
        y: int
        name: Optional[str] = None

    @dataclass
    class DataclassWithDictPayload:
        name: str
        payload: dict

    @pytest.mark.parametrize(
        'value, expected',
        (
            (Point(10, 20), b'{"x":10,"y":20,"name":null}'),
            (Point(10, 20, 'A point'), b'{"x":10,"y":20,"name":"A point"}'),
            (
                DataclassWithDictPayload(
                    'Some str here', {
                        'int': 123,
                        'float': 123.123,
                        'str': 'str',
                        'list': [1, 2, 3],
                        'dict': {'a': 1, 'b': 2},
                        'dataclass': Point(10, 20)
                    }
                ),
                b'{"name":"Some str here","payload":{"int":123,'
                b'"float":123.123,"str":"str","list":[1,2,3],'
                b'"dict":{"a":1,"b":2},"dataclass":'
                b'{"x":10,"y":20,"name":null}}}'
            ),
        )
    )
    def test_convert_dataclass_to_bytes(value, expected):
        assert convert_to_bytes(value) == expected


@pytest.mark.parametrize(
    'value', (None, [1, 2, 3], (1, 2), ['str_in_list'])
)
def test_convert_to_bytes_with_exception(value):
    with pytest.raises(TypeError):
        convert_to_bytes(value)
