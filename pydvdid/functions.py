"""Implements the public compute function and supporting 'private' functions.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from datetime import datetime
from os import listdir
from os.path import (
    basename, getctime, getsize, isdir, isfile, join
)
from struct import pack_into
from .crc64calculator import _Crc64Calculator
from .exceptions import (
    FileContentReadException, FileTimeOutOfRangeException, PathDoesNotExistException
)


def compute(dvd_path):
    """Computes a Windows API IDvdInfo2::GetDiscID-compatible 64-bit Cyclic Redundancy Check
       checksum from the DVD .vob, .ifo and .bup files found in the supplied DVD path.
    """

    _check_dvd_path_exists(dvd_path)

    _check_video_ts_path_exists(dvd_path)

    # the polynomial used for this CRC-64 checksum is:
    # x^63 + x^60 + x^57 + x^55 + x^54 + x^50 + x^49 + x^46 + x^41 + x^38 + x^37 + x^34 + x^32 +
    # x^31 + x^30 + x^28 + x^25 + x^24 + x^21 + x^16 + x^13 + x^12 + x^11 + x^8 + x^7 + x^5 + x^2
    calculator = _Crc64Calculator(0x92c64265d32139a4)

    for video_ts_file_path in _get_video_ts_file_paths(dvd_path):
        calculator.update(_get_file_creation_time(video_ts_file_path))
        calculator.update(_get_file_size(video_ts_file_path))
        calculator.update(_get_file_name(video_ts_file_path))

    calculator.update(_get_vmgi_file_content(dvd_path))
    calculator.update(_get_vts01i_file_content(dvd_path))

    return calculator.crc64


def _check_dvd_path_exists(dvd_path):
    """Raises an exception if the specified DVD path does not exist.
    """

    if not isdir(dvd_path):
        raise PathDoesNotExistException(dvd_path)


def _check_video_ts_path_exists(dvd_path):
    """Raises an exception if the specified DVD path does not contain a VIDEO_TS folder.
    """

    video_ts_folder_path = join(dvd_path, "VIDEO_TS")

    if not isdir(video_ts_folder_path):
        raise PathDoesNotExistException(video_ts_folder_path)


def _get_video_ts_file_paths(dvd_path):
    """Returns a sorted list of paths for files contained in th VIDEO_TS folder of the specified
       DVD path.
    """

    video_ts_folder_path = join(dvd_path, "VIDEO_TS")

    video_ts_file_paths = []

    for video_ts_folder_content_name in listdir(video_ts_folder_path):
        video_ts_folder_content_path = join(video_ts_folder_path, video_ts_folder_content_name)

        if isfile(video_ts_folder_content_path):
            video_ts_file_paths.append(video_ts_folder_content_path)

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
    pack_into(b"Q", file_creation_time, 0, creation_time_filetime)

    return file_creation_time


def _convert_timedelta_to_seconds(timedelta):
    """Returns the total seconds calculated from the supplied timedelta.

       (Function provided to enable running on Python 2.6 which lacks timedelta.total_seconds()).
    """

    days_in_seconds = timedelta.days * 24 * 3600
    return int((timedelta.microseconds + (timedelta.seconds + days_in_seconds) * 10 ** 6) / 10 ** 6)


def _get_file_size(file_path):
    """Returns the size of the file at the specified file path, formatted as a 4-byte unsigned
       integer bytearray.
    """

    size = getsize(file_path)

    file_size = bytearray(4)
    pack_into(b"I", file_size, 0, size)

    return file_size


def _get_file_name(file_path):
    """Returns the name of the file at the specified file path, formatted as a UTF-8 bytearray
       terminated with a null character.
    """

    file_name = basename(file_path)

    utf8_file_name = bytearray(file_name, "utf8")
    utf8_file_name.append(0)

    return utf8_file_name


def _get_vmgi_file_content(dvd_path):
    """Returns the first 65536 bytes (or the file size, whichever is smaller) of the VIDEO_TS.IFO
       file in the VIDEO_TS folder of the specified DVD path, as a bytearray.
    """

    vmgi_file_path = join(dvd_path, "VIDEO_TS", "VIDEO_TS.IFO")

    return _get_first_64k_content(vmgi_file_path)


def _get_vts01i_file_content(dvd_path):
    """Returns the first 65536 (or the file size, whichever is smaller) bytes of the VTS_01_0.IFO
       file in the VIDEO_TS folder of the specified DVD path, as a bytearray.
    """

    vts01i_file_path = join(dvd_path, "VIDEO_TS", "VTS_01_0.IFO")

    return _get_first_64k_content(vts01i_file_path)


def _get_first_64k_content(file_path):
    """Returns the first 65536 (or the file size, whichever is smaller) bytes of the file at the
       specified file path, as a bytearray.
    """

    if not isfile(file_path):
        raise PathDoesNotExistException(file_path)

    file_size = getsize(file_path)

    content_size = min(file_size, 0x10000)

    content = bytearray(content_size)
    with open(file_path, "rb") as file_object:
        content_read = file_object.readinto(content)

        if content_read is None or content_read < content_size:
            raise FileContentReadException(content_size, content_read)

    return content
