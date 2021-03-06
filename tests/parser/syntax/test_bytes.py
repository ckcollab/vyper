import pytest
from pytest import raises

from vyper import compiler
from vyper.exceptions import TypeMismatchException


fail_list = [
    """
@public
def baa():
    x: bytes[50]
    y: bytes[50]
    z = x + y
    """,
    """
@public
def baa():
    x: bytes[50]
    y: int128
    y = x
    """,
    """
@public
def baa():
    x: bytes[50]
    y: int128
    x = y
    """,
    """
@public
def baa():
    x: bytes[50]
    y: bytes[60]
    x = y
    """,
    """
@public
def foo(x: bytes[100]) -> bytes[75]:
    return x
    """,
    """
@public
def foo(x: bytes[100]) -> int128:
    return x
    """,
    """
@public
def foo(x: int128) -> bytes[75]:
    return x
    """,
    """
@public
def foo() -> bytes[10]:
    x: bytes[10] = '0x1234567890123456789012345678901234567890'
    x = 0x1234567890123456789012345678901234567890
    """,
    """
@public
def foo() -> bytes[10]:
    return "badmintonzz"
    """
]


@pytest.mark.parametrize('bad_code', fail_list)
def test_bytes_fail(bad_code):

    with raises(TypeMismatchException):
        compiler.compile(bad_code)


valid_list = [
    """
@public
def foo(x: bytes[100]) -> bytes[100]:
    return x
    """,
    """
@public
def foo(x: bytes[100]) -> bytes[150]:
    return x
    """,
    """
@public
def convert2(inp: uint256) -> bytes32:
    return convert(inp, 'bytes32')
    """,
    """
@public
def baa():
    x: bytes[50]
    """
]


@pytest.mark.parametrize('good_code', valid_list)
def test_bytes_success(good_code):
    assert compiler.compile(good_code) is not None
