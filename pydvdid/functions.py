"""Implements the public compute function and supporting 'private' functions.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from datetime import datetime
from os import listdir
from os.path import getctime, isdir, isfile, join
#basename, getsize
from struct import pack_into
from .crc64calculator import _Crc64Calculator
from .exceptions import (
    FileTimeOutOfRangeException,
    PathDoesNotExistException
)

def compute(dvd_path):
    """Computes a Windows API IDvdInfo2::GetDiscID-compatible 64-bit Cyclic Redundancy Check
       checksum from the DVD .vob, .ifo and .bup files found in the supplied DVD path.
    """

    _check_dvd_path_exists(dvd_path)

    _check_video_ts_path_exists(dvd_path)

    # the polynomial used for this checksum is:
    # x^63 + x^60 + x^57 + x^55 + x^54 + x^50 + x^49 + x^46 + x^41 + x^38 + x^37 + x^34 + x^32 +
    # x^31 + x^30 + x^28 + x^25 + x^24 + x^21 + x^16 + x^13 + x^12 + x^11 + x^8 + x^7 + x^5 + x^2
    calculator = _Crc64Calculator(0x92c64265d32139a4)

    for video_ts_file_path in _get_video_ts_file_paths(dvd_path):
        calculator.update(_get_file_creation_time(video_ts_file_path))
#        calculator.update(_get_file_size(video_ts_file_path))
#        calculator.update(_get_file_name(video_ts_file_path))

    return calculator.crc64


def _check_dvd_path_exists(dvd_path):
    """Raises an exception if the specified DVD path does not exist.
    """

    if isdir(dvd_path) == False:
        raise PathDoesNotExistException(dvd_path)


def _check_video_ts_path_exists(dvd_path):
    """Raises an exception if the specified DVD path does not contain a VIDEO_TS folder.
    """

    video_ts_path = join(dvd_path, "VIDEO_TS")

    if isdir(video_ts_path) == False:
        raise PathDoesNotExistException(video_ts_path)


def _get_video_ts_file_paths(dvd_path):
    """Returns a sorted list of paths for files contained in th VIDEO_TS folder of the specified
       DVD path.
    """

    video_ts_files_path = join(dvd_path, "VIDEO_TS")

    video_ts_paths = listdir(video_ts_files_path)

    video_ts_file_paths = [path for path in video_ts_paths if isfile(path)]

    return sorted(video_ts_file_paths)


def _get_file_creation_time(file_path):
    """Returns the creation time of the file at the specified file path in Microsoft FILETIME
       structure format (https://msdn.microsoft.com/en-us/library/windows/desktop/ms724284.aspx),
       formatted as a 8-byte unsigned integer bytearray.
    """

    ctime = getctime(file_path)

    if ctime < -11644473600 or ctime >= 253402300800:
        raise FileTimeOutOfRangeException(ctime)

    creation_time_datetime = datetime.utcfromtimestamp(ctime)

    creation_time_epoch_offset = creation_time_datetime - datetime(1601, 1, 1)

    creation_time_secs_from_epoch = _convert_timedelta_to_seconds(creation_time_epoch_offset)

    creation_time_filetime = int(creation_time_secs_from_epoch * (10 ** 7))

    file_creation_time = bytearray(8)
    pack_into("Q", file_creation_time, 0, creation_time_filetime)

    return file_creation_time


def _convert_timedelta_to_seconds(timedelta):
    """Returns the total seconds calculated from the supplied timedelta.

       (Function provided to enable running on Python 2.6 which lacks timedelta.total_seconds()).
    """

    days_in_seconds = timedelta.days * 24 * 3600
    return (timedelta.microseconds + (timedelta.seconds + days_in_seconds) * 10 ** 6) / 10 ** 6


#def _get_file_size(file_path):
#    """Returns the size of the file at the specified file path, formatted as a 4-byte unsigned
#       integer byte string.
#    """
#
#    file_size = getsize(file_path)
#
#    return pack("I", file_size)


#def _get_file_name(file_path):
#    """Returns the name of the file at the specified file path, formatted as a UTF-8 string
#       terminated with a null character.
#    """
#
#    file_name = basename(file_path)
#
#    utf8_file_name = file_name.encode(b"utf-8")
#
#    return utf8_file_name + b"\x00"
