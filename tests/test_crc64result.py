"""Module contains the TestCrc64Result class.
"""

from unittest import TestCase

from pydvdid.Crc64Result import Crc64Result

class TestCrc64Result(TestCase):
    """Class contains tests for the pydvdid.Crc64Result class.
    """

    def test___init__(self):
        """Test that initialisation sets the 'private' __crc member to that of the argument
        (accesses member through name mangling).
        """
        result = Crc64Result(2246800662182009355)
        # pylint: disable=locally-disabled, no-member, protected-access
        self.assertEqual(result._Crc64Result__crc, 2246800662182009355)

    def test_high_bytes(self):
        """Test that invokation returns the topmost 4 bytes, formatted as a lowercase hex string.
        """
        result = Crc64Result(2246800662182009355)
        self.assertEqual(result.high_bytes, "1f2e3d4c")

    def test_low_bytes(self):
        """Test that invokation returns the bottommost 4 bytes, formatted as a lowercase hex string.
        """
        result = Crc64Result(2246800662182009355)
        self.assertEqual(result.low_bytes, "56789a0b")

    def test___str__(self):
        """Test that invokation returns the the full crc, formated as a lowercase hex string.
        """
        result = Crc64Result(2246800662182009355)
        self.assertEqual(result.__str__(), "1f2e3d4c56789a0b")
