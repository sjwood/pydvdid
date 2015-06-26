"""Implements the public compute function and supporting 'private' functions.
"""


from __future__ import absolute_import
from os.path import isdir, join
from .exceptions import DvdPathDoesNotExistException, VideoTsPathDoesNotExistException


def compute(dvd_path):
    """Computes a Windows API IDvdInfo2::GetDiscID-compatible 64-bit Cyclic Redundancy Check
       checksum from the DVD .vob, .ifo and .bup files found in the supplied DVD path.
    """

    _check_dvd_path_exists(dvd_path)

    _check_video_ts_path_exists(dvd_path)


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
