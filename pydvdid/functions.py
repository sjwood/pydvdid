"""Implements the public compute function and supporting 'private' functions.
"""


from __future__ import absolute_import
from glob import glob
from os.path import isdir, join
from .crc64calculator import _Crc64Calculator
from .exceptions import DvdPathDoesNotExistException, VideoTsPathDoesNotExistException


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
        print video_ts_file_path

    return calculator.crc64


def _check_dvd_path_exists(dvd_path):
    """Raises an exception if the specified DVD path does not exist.
    """

    if isdir(dvd_path) == False:
        raise DvdPathDoesNotExistException("Path '{0}' does not exist.".format(dvd_path))


def _check_video_ts_path_exists(dvd_path):
    """Raises an exception if the specified DVD path does not contain a VIDEO_TS folder.
    """

    video_ts_path = join(dvd_path, "VIDEO_TS")

    if isdir(video_ts_path) == False:
        raise VideoTsPathDoesNotExistException("Path '{0}' does not exist.".format(video_ts_path))


def _get_video_ts_file_paths(dvd_path):
    """Returns a sorted list of paths for files contained in th VIDEO_TS folder of the specified
       DVD path.
    """

    video_ts_files_path = join(dvd_path, "VIDEO_TS", "*")

    return sorted(glob(video_ts_files_path))
