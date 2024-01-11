# © 2024 Fraunhofer-Gesellschaft e.V., München
# © 2024 Fraunhofer-Gesellschaft e.V., M├╝nchen
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# pylint: disable=disallowed-name

from string_order import StringOrder


def test_construction():
    foo = StringOrder('foo')
    assert foo is not None


def test_eq():
    foo1 = StringOrder('foo')
    foo2 = StringOrder('foo')
    assert foo1 == foo2


def test_lt():
    foo = StringOrder('foo')
    baa = StringOrder('baa')
    assert foo > baa
