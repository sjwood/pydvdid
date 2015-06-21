from unittest import TestCase

from pydvdid import Crc64Result

class TestCrc64Result(TestCase):
    def test___init__(self):
        # test that initialisation sets the 'private' __crc member to the argument
        result = Crc64Result(104717)
        self.assertEqual(result._Crc64Result__crc, 104717)
