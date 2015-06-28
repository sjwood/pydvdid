"""Implements the TestCrc64Result class.
"""


from __future__ import absolute_import
from mock import Mock, patch
from unittest import TestCase
from pydvdid.crc64result import Crc64Result


class TestCrc64Result(TestCase):
    """Implements a class that contains tests for the pydvdid.crc64result module.
    """

    def test_crc64result___init___sets_private_variables(self): # pylint: disable=locally-disabled, invalid-name
        """Test that initialisation of a Crc64Result instance sets the 'private' _crc64 member to
           that of the argument.
        """

        result = Crc64Result(2246800662182009355)

        self.assertEqual(2246800662182009355, result._crc64) # pylint: disable=locally-disabled, protected-access


    @patch("pydvdid.crc64result.Crc64Result.__init__", Mock(return_value=None))
    def test_crc64result_high_bytes_returns_correct_value(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of high_bytes returns the topmost 4 bytes of _crc64, formatted as a
           lowercase hex string.
        """

        result = Crc64Result(0)
        result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

        self.assertEqual("1f2e3d4c", result.high_bytes)


    @patch("pydvdid.crc64result.Crc64Result.__init__", Mock(return_value=None))
    def test_crc64result_low_bytes_returns_correct_value(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of low_bytes returns the bottommost 4 bytes of _crc64, formatted as
           a lowercase hex string.
        """

        result = Crc64Result(0)
        result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

        self.assertEqual("56789a0b", result.low_bytes)


    @patch("pydvdid.crc64result.Crc64Result.__init__", Mock(return_value=None))
    def test_crc64result___eq___returns_True_when_instances_are_equal(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of == returns True when two instances of Crc64Result have the same
           _crc64 value.
        """

        first = Crc64Result(0)
        first._crc64 = 7549347567549 # pylint: disable=locally-disabled, protected-access
        second = Crc64Result(1)
        second._crc64 = 7549347567549 # pylint: disable=locally-disabled, protected-access

        self.assertEqual(first == second, True)


    @patch("pydvdid.crc64result.Crc64Result.__init__", Mock(return_value=None))
    def test_crc64result___eq___returns_False_when_instances_are_not_equal(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of == returns False when two instances of Crc64Result have
           different _crc64 values.
        """

        first = Crc64Result(0)
        first._crc64 = 93005 # pylint: disable=locally-disabled, protected-access
        second = Crc64Result(0)
        second._crc64 = 22050968374385 # pylint: disable=locally-disabled, protected-access

        self.assertEqual(first == second, False)


    @patch("pydvdid.crc64result.Crc64Result.__init__", Mock(return_value=None))
    def test_crc64result___ne___returns_False_when_instances_are_equal(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of != returns False when two instances of Crc64Result have the same
           _crc64 values.
        """

        first = Crc64Result(0)
        first._crc64 = 12 # pylint: disable=locally-disabled, protected-access
        second = Crc64Result(1)
        second._crc64 = 12 # pylint: disable=locally-disabled, protected-access

        self.assertEqual(first != second, False)


    @patch("pydvdid.crc64result.Crc64Result.__init__", Mock(return_value=None))
    def test_crc64result___ne___returns_True_when_instances_are_not_equal(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of != returns True when two instances of Crc64Result have different
           _crc64 values.
        """

        first = Crc64Result(0)
        first._crc64 = 848485484364545884 # pylint: disable=locally-disabled, protected-access
        second = Crc64Result(0)
        second._crc64 = 66307593 # pylint: disable=locally-disabled, protected-access

        self.assertEqual(first != second, True)


    @patch("pydvdid.crc64result.Crc64Result.__init__", Mock(return_value=None))
    def test_crc64result___str___returns_correct_value(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of str() returns the the full _crc64 value, formated as a lowercase
           hex string.
        """

        result = Crc64Result(0)
        result._crc64 = 2246800662182009355 # pylint: disable=locally-disabled, protected-access

        self.assertEqual("1f2e3d4c56789a0b", str(result))
