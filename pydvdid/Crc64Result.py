"""Module contains the Crc64Result class.
"""

class Crc64Result(object):
    """Class represents the result of a 64-bit Cyclic Redundancy Check checksum.
    """

    def __init__(self, crc):
        self.__crc = crc

    @property
    def high_bytes(self):
        """Returns the topmost 4 bytes of the checksum formatted as a lowercase hex string.
        """
        return format(self.__crc >> 32, "08x")

    @property
    def low_bytes(self):
        """Returns the bottommost 4 bytes of the checksum formatted as a lowercase hex string.
        """
        return format(self.__crc & 0xffffffff, "08x")

    def __str__(self):
        return format(self.__crc, "016x")
