"""Implements the TestCrc64Result class.
"""


from __future__ import absolute_import
from unittest import TestCase
from pydvdid.crc64result import Crc64Result


class TestCrc64Result(TestCase):
    """Implements a class that contains tests for the pydvdid.crc64result module.
    """

    def test_crc64result___init___sets_private_variables(self): # pylint: disable=locally-disabled, invalid-name
        """Test that initialisation of a Crc64Result instance sets the 'private' __crc member to
           that of the argument (accesses member through name mangling).
        """

        result = Crc64Result(2246800662182009355)
        self.assertEqual(2246800662182009355, result._Crc64Result__crc) # pylint: disable=locally-disabled, no-member, protected-access


    def test_crc64result_high_bytes_returns_correct_value(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of high_bytes returns the topmost 4 bytes, formatted as a lowercase
           hex string.
        """

        result = Crc64Result(2246800662182009355)
        self.assertEqual("1f2e3d4c", result.high_bytes)


    def test_crc64result_low_bytes_returns_correct_value(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of low_bytes returns the bottommost 4 bytes, formatted as a
           lowercase hex string.
        """

        result = Crc64Result(2246800662182009355)
        self.assertEqual("56789a0b", result.low_bytes)


    def test_crc64result___eq___returns_True_when_instances_are_equal(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of == returns True when two instances of Crc64Result have the same
           __crc64 value.
        """

        first = Crc64Result(7549347567549)
        second = Crc64Result(7549347567549)

        self.assertEqual(first == second, True)


    def test_crc64result___eq___returns_False_when_instances_are_not_equal(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of == returns False when two instances of Crc64Result have
           different __crc64 values.
        """

        first = Crc64Result(93005)
        second = Crc64Result(22050968374385)

        self.assertEqual(first == second, False)


    def test_crc64result___ne___returns_False_when_instances_are_equal(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of != returns False when two instances of Crc64Result have the same
           __crc64 values.
        """

        first = Crc64Result(12)
        second = Crc64Result(12)

        self.assertEqual(first != second, False)


    def test_crc64result___ne___returns_True_when_instances_are_not_equal(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of != returns True when two instances of Crc64Result have different
           __crc64 values.
        """

        first = Crc64Result(848485484364545884)
        second = Crc64Result(66307593)

        self.assertEqual(first != second, True)


    def test_crc64result___str___returns_correct_value(self): # pylint: disable=locally-disabled, invalid-name
        """Test that invocation of str() returns the the full crc, formated as a lowercase hex
           string.
        """

        result = Crc64Result(2246800662182009355)
        self.assertEqual("1f2e3d4c56789a0b", str(result))
