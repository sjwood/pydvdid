"""Implements tests for the pydvdid.crc64result module.
"""


from __future__ import absolute_import
from mock import call, patch
from nose.tools import eq_, istest
from pydvdid.crc64result import Crc64Result


@istest
def crc64result___init___sets_private_variables(): # pylint: disable=locally-disabled, invalid-name
    """Test that initialisation of a Crc64Result instance sets the 'private' _crc64 member to that
       of the argument.
    """

    result = Crc64Result(2246800662182009355)

    eq_(2246800662182009355, result._crc64) # pylint: disable=locally-disabled, protected-access


@istest
@patch("pydvdid.crc64result.Crc64Result.__init__")
def crc64result_high_bytes_returns_correct_value(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Test that invocation of high_bytes returns the topmost 4 bytes of _crc64, formatted as a
       lowercase hex string.
    """

    mock_init.return_value = None

    result = Crc64Result(0x3af1)
    result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

    eq_("1f2e3d4c", result.high_bytes)

    mock_init.assert_called_once_with(0x3af1)


@istest
@patch("pydvdid.crc64result.Crc64Result.__init__")
def crc64result_low_bytes_returns_correct_value(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Test that invocation of low_bytes returns the bottommost 4 bytes of _crc64, formatted as a
       lowercase hex string.
    """

    mock_init.return_value = None

    result = Crc64Result(0x88889999)
    result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

    eq_("56789a0b", result.low_bytes)

    mock_init.assert_called_once_with(0x88889999)


@istest
@patch("pydvdid.crc64result.Crc64Result.__init__")
def crc64result___eq___returns_True_when_instances_are_equal(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Test that invocation of == returns True when two instances of Crc64Result have the same
       _crc64 value.
    """

    mock_init.return_value = None

    first = Crc64Result(0x2944)
    first._crc64 = 7549347567549 # pylint: disable=locally-disabled, protected-access
    second = Crc64Result(0xcc10)
    second._crc64 = 7549347567549 # pylint: disable=locally-disabled, protected-access

    eq_(first == second, True)

    mock_init.assert_has_calls([call(0x2944), call(0xcc10)])


@istest
@patch("pydvdid.crc64result.Crc64Result.__init__")
def crc64result___eq___returns_False_when_instances_are_not_equal(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Test that invocation of == returns False when two instances of Crc64Result have different
       _crc64 values.
    """

    mock_init.return_value = None

    first = Crc64Result(0x1d)
    first._crc64 = 93005 # pylint: disable=locally-disabled, protected-access
    second = Crc64Result(0x1d)
    second._crc64 = 22050968374385 # pylint: disable=locally-disabled, protected-access

    eq_(first == second, False)

    mock_init.assert_has_calls([call(0x1d), call(0x1d)])


@istest
@patch("pydvdid.crc64result.Crc64Result.__init__")
def crc64result___ne___returns_False_when_instances_are_equal(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Test that invocation of != returns False when two instances of Crc64Result have the same
       _crc64 values.
    """

    mock_init.return_value = None

    first = Crc64Result(0x4410)
    first._crc64 = 12 # pylint: disable=locally-disabled, protected-access
    second = Crc64Result(0xba11)
    second._crc64 = 12 # pylint: disable=locally-disabled, protected-access

    eq_(first != second, False)

    mock_init.assert_has_calls([call(0x4410), call(0xba11)])


@istest
@patch("pydvdid.crc64result.Crc64Result.__init__")
def crc64result___ne___returns_True_when_instances_are_not_equal(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Test that invocation of != returns True when two instances of Crc64Result have different
       _crc64 values.
    """

    mock_init.return_value = None

    first = Crc64Result(0)
    first._crc64 = 848485484364545884 # pylint: disable=locally-disabled, protected-access
    second = Crc64Result(0)
    second._crc64 = 66307593 # pylint: disable=locally-disabled, protected-access

    eq_(first != second, True)


@istest
@patch("pydvdid.crc64result.Crc64Result.__init__")
def crc64result___str___returns_correct_value(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Test that invocation of str() returns the the full _crc64 value, formated as a lowercase hex
       string.
    """

    mock_init.return_value = None

    result = Crc64Result(0xd00d)
    result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

    eq_("1f2e3d4c56789a0b", str(result))

    mock_init.assert_called_once_with(0xd00d)
