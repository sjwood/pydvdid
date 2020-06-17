"""Implements the public compute function and supporting 'private' functions.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from datetime import datetime
from dateutil.tz import tzoffset
from io import BytesIO
from os import listdir
from os.path import (
    basename, getctime, getsize, isdir, isfile, join
)
from struct import pack_into
import pycdlib
from .crc64calculator import _Crc64Calculator
from .exceptions import (
    FileContentReadException, FileTimeOutOfRangeException, PathDoesNotExistException
)


def compute(dvd_path):
    """Computes a Windows API IDvdInfo2::GetDiscID-compatible 64-bit Cyclic Redundancy Check
       checksum from the DVD .vob, .ifo and .bup files found in the supplied DVD path.
    """

    dvd = pycdlib.PyCdlib()

    try:
        dvd.open(dvd_path)
    except:
        raise FileContentReadException(dvd_path)

    _check_video_ts_path_exists(dvd)

    # the polynomial used for this CRC-64 checksum is:
    # x^63 + x^60 + x^57 + x^55 + x^54 + x^50 + x^49 + x^46 + x^41 + x^38 + x^37 + x^34 + x^32 +
    # x^31 + x^30 + x^28 + x^25 + x^24 + x^21 + x^16 + x^13 + x^12 + x^11 + x^8 + x^7 + x^5 + x^2
    calculator = _Crc64Calculator(0x92c64265d32139a4)

    for vob, file_path in _get_video_ts_files(dvd):
        calculator.update(_get_file_creation_time(vob))
        calculator.update(_get_file_size(vob))
        calculator.update(_get_file_name(file_path))
    for vob, file_path in _get_video_ts_files(dvd):
        if basename(file_path) in ["VIDEO_TS.IFO", "VTS_01_0.IFO"]:
            calculator.update(_get_first_64k_content(dvd, vob))

    return calculator.crc64


def _check_video_ts_path_exists(dvd):
    """Raises an exception if the specified DVD path does not contain a VIDEO_TS folder.
    """

    files = dvd.list_children(iso_path="/VIDEO_TS")
    if not files:
        raise PathDoesNotExistException("/VIDEO_TS")


def _get_video_ts_files(dvd):
    """Returns a sorted list of paths for files contained in the VIDEO_TS folder of the specified
       DVD path.
    """

    for vob in dvd.list_children(iso_path="/VIDEO_TS"):
        file_path = vob.file_identifier().decode()
        # skip the `.` and `..` paths
        if file_path in [".", ".."]:
            continue
        # remove the semicolon and version number
        if ";" in file_path:
            file_path = file_path.split(";")[0]
        # join it to root to be absolute
        file_path = join("/VIDEO_TS", file_path)
        # we can just yield, it's already in a good enough order
        yield vob, file_path


def _get_file_creation_time(vob):
    """Returns the creation time of the file at the specified file path in Microsoft FILETIME
       structure format (https://msdn.microsoft.com/en-us/library/windows/desktop/ms724284.aspx),
       formatted as a 8-byte unsigned integer bytearray.
    """

    dt = datetime(
        year=1900 + vob.date.years_since_1900, month=vob.date.month, day=vob.date.day_of_month,
        hour=vob.date.hour, minute=vob.date.minute, second=vob.date.second,
        # offset the timezone, since ISO's dates are offsets of GMT in 15 minute intervals, we
        # need to calculate that but in seconds to pass to tzoffset.
        tzinfo=tzoffset("GMT", (15 * vob.date.gmtoffset) * 60)
    )

    epoch_offset = dt - datetime(1601, 1, 1, tzinfo=tzoffset(None, 0))

    secs_from_epoch = _convert_timedelta_to_seconds(epoch_offset)

    creation_time_filetime = int(secs_from_epoch * (10 ** 7))

    file_creation_time = bytearray(8)
    pack_into(b"Q", file_creation_time, 0, creation_time_filetime)

    return file_creation_time


def _convert_timedelta_to_seconds(timedelta):
    """Returns the total seconds calculated from the supplied timedelta.

       (Function provided to enable running on Python 2.6 which lacks timedelta.total_seconds()).
    """

    days_in_seconds = timedelta.days * 24 * 3600
    return int((timedelta.microseconds + (timedelta.seconds + days_in_seconds) * 10 ** 6) / 10 ** 6)


def _get_file_size(vob):
    """Returns the size of the file at the specified file path, formatted as a 4-byte unsigned
       integer bytearray.
    """

    size = vob.get_data_length()

    file_size = bytearray(4)
    pack_into(b"I", file_size, 0, size)

    return file_size


def _get_file_name(vob):
    """Returns the name of the file at the specified file path, formatted as a UTF-8 bytearray
       terminated with a null character.
    """

    file_name = basename(vob)

    utf8_file_name = bytearray(file_name, "utf8")
    utf8_file_name.append(0)

    return utf8_file_name


def _get_first_64k_content(dvd, vob):
    """Returns the first 65536 (or the file size, whichever is smaller) bytes of the file at the
       specified file path, as a bytearray.
    """

    read_size = min(vob.get_data_length(), 0x10000)

    # perhaps find a way to read a specific amount of bytes rather than the full file
    # i dont see a way to without having to grab the lba and manually read with a device
    # handle, which is like kinda eww -git/rlaPHOENiX ; todo
    f = BytesIO()
    dvd.get_file_from_iso_fp(
        outfp=f,
        iso_path=f"/VIDEO_TS/{vob.file_identifier().decode()}"
    )
    f.seek(0)  # go back to start after writing data above
    content = f.read(read_size)

    if content is None or len(content) < read_size:
        raise FileContentReadException(read_size, content)

    return content
