"""Implements the Crc64Result class.
"""


from __future__ import unicode_literals


class Crc64Result(object):
    """Implements a class that represents the result of a 64-bit Cyclic Redundancy Check checksum.
    """

    def __init__(self, crc64):
        self._crc64 = crc64


    @property
    def high_bytes(self):
        """Returns the topmost 4 bytes of the checksum formatted as a lowercase hex string.
        """

        return format(self._crc64 >> 32, "08x")


    @property
    def low_bytes(self):
        """Returns the bottommost 4 bytes of the checksum formatted as a lowercase hex string.
        """

        return format(self._crc64 & 0xffffffff, "08x")


    def __eq__(self, other):
        return self._crc64 == other._crc64 # pylint: disable=locally-disabled, protected-access


    def __ne__(self, other):
        return not self.__eq__(other)


    def __str__(self):
        return format(self._crc64, "016x")
