"""Implements tests for the pydvdid.crc64result module.
"""


from __future__ import absolute_import
from sys import modules
from mock import call, patch
from nose_parameterized import parameterized, param
from nose.tools import eq_, istest, nottest
from pydvdid.crc64result import Crc64Result


@istest
def crc64result___init___sets_private_variables(): # pylint: disable=locally-disabled, invalid-name
    """Tests that initialisation of a Crc64Result instance sets the 'private' _crc64 member to that
       of the argument.
    """

    result = Crc64Result(2246800662182009355)

    eq_(2246800662182009355, result._crc64) # pylint: disable=locally-disabled, protected-access


@istest
@patch(b"pydvdid.crc64result.Crc64Result.__init__")
def crc64result_high_bytes_returns_correct_value(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of high_bytes returns the topmost 4 bytes of _crc64, formatted as a
       lowercase hex string.
    """

    mock_init.return_value = None

    result = Crc64Result(0x3af1)
    result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

    eq_(b"1f2e3d4c", result.high_bytes)

    mock_init.assert_called_once_with(0x3af1)


@istest
@patch(b"pydvdid.crc64result.Crc64Result.__init__")
def crc64result_low_bytes_returns_correct_value(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of low_bytes returns the bottommost 4 bytes of _crc64, formatted as a
       lowercase hex string.
    """

    mock_init.return_value = None

    result = Crc64Result(0x88889999)
    result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

    eq_(b"56789a0b", result.low_bytes)

    mock_init.assert_called_once_with(0x88889999)


@istest
@parameterized([
    param(b"a == b is True", 1, 1001, 2, 1001, b"_equality_comparison", True),
    param(b"a == b is False", 4, 2001, 4, 4001, b"_equality_comparison", False),
    param(b"a != b is False", 8, 8001, 16, 8001, b"_inequality_comparison", False),
    param(b"a != b is True", 32, 16001, 32, 32001, b"_inequality_comparison", True)
])
@patch(b"pydvdid.crc64result.Crc64Result.__init__") # pylint: disable=locally-disabled, invalid-name, too-many-arguments
def crc64result_equality_and_inequality_comparisons_return_correctly(description, polynomial_one,
                                                                     crc64_one, polynomial_two,
                                                                     crc64_two,
                                                                     comparison_function_name,
                                                                     expected, mock_init):
    """Tests that invocation of == and != equality comparisons return correctly.

       (This is a Nose generator test which receives a set of data provided by nose-parameterized).
    """

    mock_init.return_value = None

    # nose-parameterized can only pass through primitives, so get function from name string
    comparison_function = _get_module_function(comparison_function_name)

    result_one = Crc64Result(polynomial_one)
    result_one._crc64 = crc64_one # pylint: disable=locally-disabled, protected-access

    result_two = Crc64Result(polynomial_two)
    result_two._crc64 = crc64_two # pylint: disable=locally-disabled, protected-access

    comparison_value = comparison_function(result_one, result_two)
    assert_message = b"Unexpected result '{0}' for test '{1}'".format(comparison_value, description)
    eq_(expected, comparison_value, assert_message)

    mock_init.assert_has_calls([
        call(polynomial_one),
        call(polynomial_two)
    ])


@nottest
def _get_module_function(function_name):
    """Returns a function from the current module whose name matches the supplied function name, or
       raises a ValueError.
    """

    if not hasattr(modules[__name__], function_name):
        raise ValueError(b"Function {0} does not exist".format(function_name))

    return getattr(modules[__name__], function_name)


@nottest
def _equality_comparison(first, second):
    """Performs a simple == equality comparison.
    """

    return first == second


@nottest
def _inequality_comparison(first, second):
    """Performs a simple != inequality comparison.
    """

    return first != second


@istest
@patch(b"pydvdid.crc64result.Crc64Result.__init__")
def crc64result___str___returns_correct_value(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of str() returns the the full _crc64 value, formated as a lowercase hex
       string.
    """

    mock_init.return_value = None

    result = Crc64Result(0xd00d)
    result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

    eq_(b"1f2e3d4c56789a0b", str(result))

    mock_init.assert_called_once_with(0xd00d)
