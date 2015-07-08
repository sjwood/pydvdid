"""Implements the _Crc64Calculator class.
"""


from __future__ import absolute_import
from .crc64result import Crc64Result


class _Crc64Calculator(object):
    """Implements a class that calculates a 64-bit Cyclic Redundancy Check checksum.

       Class initialiser requires a polynomial to seed the construction of a lookup table and an
       optional initial XOR value.
    """

    def __init__(self, polynomial, initial_xor=0xffffffffffffffff):
        self._construct_lookup_table(polynomial)
        self._crc64 = initial_xor


    @property
    def crc64(self):
        """Returns the current CRC-64.
        """

        return Crc64Result(self._crc64)


    def update(self, content):
        """Enumerates the bytes of the supplied bytearray and updates the CRC-64.
           No return value.
        """

        for byte in content:
            self._crc64 = (self._crc64 >> 8) ^ self._lookup_table[(self._crc64 & 0xff) ^ byte]


    def _construct_lookup_table(self, polynomial):
        """Precomputes a CRC-64 lookup table seeded from the supplied polynomial.
           No return value.
        """

        self._lookup_table = []

        for i in range(0, 256):
            lookup_value = i

            for _ in range(0, 8):
                if lookup_value & 0x1 == 0x1:
                    lookup_value = (lookup_value >> 1) ^ polynomial

                else:
                    lookup_value = lookup_value >> 1

            self._lookup_table.append(lookup_value)
