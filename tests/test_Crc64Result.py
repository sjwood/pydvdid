from unittest import TestCase

from pydvdid import Crc64Result

class TestCrc64Result(TestCase):
    def test___init__(self):
        # test that initialisation sets the 'private' __crc member to the argument
        result = Crc64Result(104717)
        self.assertEqual(result._Crc64Result__crc, 104717)

    def test_high_bytes(self):
        # test that invokation returns the topmost 4 bytes, formated as a lowercase hex string
        result = Crc64Result(2246800662182009355)
        self.assertEqual(result.high_bytes, "1f2e3d4c")

    def test_low_bytes(self):
        # test that invokation returns the bottommost 4 bytes, formated as a lowercase hex string
        result = Crc64Result(2246800662182009355)
        self.assertEqual(result.low_bytes, "56789a0b")

    def test___str__(self):
        # test that invokation returns the the full crc, formated as a lowercase hex string
        result = Crc64Result(2246800662182009355)
        self.assertEqual(result.__str__(), "1f2e3d4c56789a0b")
