# pylint: disable=disallowed-name

from reverser import Reverser


def test_construction():
    foo = Reverser('foo')
    assert foo is not None


def test_eq():
    foo1 = Reverser('foo')
    foo2 = Reverser('foo')
    assert foo1 == foo2


def test_lt():
    foo = Reverser('foo')
    baa = Reverser('baa')
    assert foo < baa
