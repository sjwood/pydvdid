"""Implements the TestCrc64Result class.
"""


from __future__ import absolute_import
from unittest import TestCase
from pydvdid import Crc64Result


class TestCrc64Result(TestCase):
    """Implements a class that contains tests for the pydvdid.crc64result module.
    """

    def test___init__(self):
        """Test that initialisation sets the 'private' __crc member to that of the argument
        (accesses member through name mangling).
        """

        result = Crc64Result(2246800662182009355)
        self.assertEqual(2246800662182009355, result._Crc64Result__crc) # pylint: disable=locally-disabled, no-member, protected-access


    def test_high_bytes(self):
        """Test that invocation returns the topmost 4 bytes, formatted as a lowercase hex string.
        """

        result = Crc64Result(2246800662182009355)
        self.assertEqual("1f2e3d4c", result.high_bytes)


    def test_low_bytes(self):
        """Test that invocation returns the bottommost 4 bytes, formatted as a lowercase hex string.
        """

        result = Crc64Result(2246800662182009355)
        self.assertEqual("56789a0b", result.low_bytes)


    def test___str__(self):
        """Test that invocation returns the the full crc, formated as a lowercase hex string.
        """

        result = Crc64Result(2246800662182009355)
        self.assertEqual("1f2e3d4c56789a0b", result.__str__())
