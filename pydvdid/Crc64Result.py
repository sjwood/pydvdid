class Crc64Result(object):
    def __init__(self, crc):
        self.__crc = crc

    @property
    def high_bytes(self):
        return format(self.__crc >> 32, "08x")

    @property
    def low_bytes(self):
        return format(self.__crc & 0xffffffff, "08x")

    def __str__(self):
        return format(self.__crc, "016x")

    def do_something(self):
        return 1
