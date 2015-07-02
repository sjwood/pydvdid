"""Implements tests for the pydvdid.functions module.
"""


from __future__ import absolute_import
from binascii import hexlify
from mock import call, patch
from nose_parameterized import parameterized, param
from nose.tools import eq_, istest, ok_
from pydvdid.exceptions import (
    FileTimeOutOfRangeException,
    PathDoesNotExistException
)
from pydvdid.functions import (
    _check_dvd_path_exists,
    _check_video_ts_path_exists,
    _get_file_creation_time,
    _get_file_name,
    _get_file_size,
    _get_video_ts_file_paths
)


@istest
@patch("pydvdid.functions.isdir")
def _check_dvd_path_exists_does_not_raise_exception_when_path_exists(mock_isdir): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _check_dvd_path_exists() with a valid path does not raise an
       exception.
    """

    mock_isdir.return_value = True

    try:
        _check_dvd_path_exists(b"DVD_PATH")
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(exception).__name__))

    mock_isdir.assert_called_once_with(b"DVD_PATH")


@istest
@patch("pydvdid.functions.isdir")
def _check_dvd_path_exists_raises_exception_when_path_does_not_exist(mock_isdir): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _check_dvd_path_exists() with an invalid path raises a
       PathDoesNotExistException exception.
    """

    mock_isdir.return_value = False

    try:
        _check_dvd_path_exists("DVD_PATH")
    except PathDoesNotExistException:
        pass
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(exception).__name__))
    else:
        ok_(False, "An exception was expected but was not raised.")

    mock_isdir.assert_called_once_with("DVD_PATH")


@istest
@patch("pydvdid.functions.isdir")
def _check_video_ts_path_exists_does_not_raise_exception_when_path_exists(mock_isdir): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _check_video_ts_path_exists() with a valid path does not raise an
       exception.
    """

    mock_isdir.return_value = True

    try:
        _check_video_ts_path_exists(b"DVD_PATH")
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(exception).__name__))

    mock_isdir.assert_called_once_with(b"DVD_PATH/VIDEO_TS")


@istest
@patch("pydvdid.functions.isdir")
def _check_video_ts_path_exists_raises_exception_when_path_does_not_exist(mock_isdir): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _check_video_ts_path_exists() with an invalid path raises a
       PathDoesNotExistException exception.
    """

    mock_isdir.return_value = False

    try:
        _check_video_ts_path_exists("DVD_PATH")
    except PathDoesNotExistException:
        pass
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(exception).__name__))
    else:
        ok_(False, "An exception was expected but was not raised.")

    mock_isdir.assert_called_once_with("DVD_PATH/VIDEO_TS")


@istest
@patch("pydvdid.functions.isfile")
@patch("pydvdid.functions.listdir")
def _get_video_ts_file_paths_returns_a_sorted_list_of_file_paths(mock_listdir, mock_isfile): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _get_video_ts_file_paths() uses listdir to get the contents of the
       VIDEO_TS folder of the specified DVD path, then uses isfile to filter out directories, then
       returns a sorted list of the file paths.
    """

    mock_listdir.return_value = [
        "DVD_PATH/VIDEO_TS/VTS_01_0.VOB",
        "DVD_PATH/VIDEO_TS/unexpected_folder",
        "DVD_PATH/VIDEO_TS/VTS_01_0.BUP",
        "DVD_PATH/VIDEO_TS/VTS_01_0.IFO"
    ]

    mock_isfile.side_effect = [True, False, True, True]

    video_ts_file_paths = _get_video_ts_file_paths("DVD_PATH")

    eq_([
        "DVD_PATH/VIDEO_TS/VTS_01_0.BUP",
        "DVD_PATH/VIDEO_TS/VTS_01_0.IFO",
        "DVD_PATH/VIDEO_TS/VTS_01_0.VOB"
    ], video_ts_file_paths)

    mock_listdir.assert_called_once_with("DVD_PATH/VIDEO_TS")

    mock_isfile.assert_has_calls([
        call("DVD_PATH/VIDEO_TS/VTS_01_0.VOB"),
        call("DVD_PATH/VIDEO_TS/unexpected_folder"),
        call("DVD_PATH/VIDEO_TS/VTS_01_0.BUP"),
        call("DVD_PATH/VIDEO_TS/VTS_01_0.IFO")
    ])


@istest
@parameterized([
    param("CTime '1600-12-31 23:59:59'", "DVD_PATH/VIDEO_TS/VIDEO_TS.BUP", -11644473601),
    param("CTime '10000-01-01 00:00:00'", "DVD_PATH/VIDEO_TS/VIDEO_TS.IFO", 253402300800)
])
@patch("pydvdid.functions.getctime") # pylint: disable=locally-disabled, invalid-name
def _get_file_creation_time_raises_exception_when_file_creation_time_is_invalid(description,
                                                                                file_path, ctime,
                                                                                mock_getctime):
    """Tests that invocation of _get_file_creation_time() with a file path that has a creation time
       that is outside the allowable range of values raises a FileTimeOutOfRangeException exception.
    """

    mock_getctime.return_value = ctime

    try:
        _get_file_creation_time(file_path)
    except FileTimeOutOfRangeException:
        pass
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        template = "Test case '{0}' failed: An unexpected {1} exception was raised."
        ok_(False, template.format(description, type(exception).__name__))
    else:
        template = "Test case '{0}' failed: An exception was expected but was not raised."
        ok_(False, template.format(description))

    mock_getctime.assert_called_once_with(file_path)


@istest
@parameterized([
    param("CTime 1601-01-01 00:00:00", "1.txt", -11644473600, "\x00\x00\x00\x00\x00\x00\x00\x00"),
    param("CTime 9999-12-31 23:59:59", "2.pdf", 253402300799, "\x80\xa9\x27\xd1\x5e\x5a\xc8\x24"),
    param("CTime 2015-07-01 21:51:43", "3.spec7", 1435787503, "\x80\x01\x23\x1e\x48\xb4\xd0\x01")
])
@patch("pydvdid.functions.getctime") # pylint: disable=locally-disabled, invalid-name
def _get_file_creation_time_returns_correctly_when_file_creation_time_is_valid(description,
                                                                               file_path, ctime,
                                                                               expected,
                                                                               mock_getctime):
    """Tests that invocation of _get_file_creation_time() with a file path that has a creation time
       that is within the allowable range of values returns correctly.
    """

    mock_getctime.return_value = ctime

    file_creation_time = _get_file_creation_time(file_path)

    template = "Test case '{0}' failed: expected '0x{1}', actual '0x{2}'."
    assert_message = template.format(description, hexlify(expected), hexlify(file_creation_time))

    eq_(expected, file_creation_time, assert_message)

    mock_getctime.assert_called_once_with(file_path)


@istest
@parameterized([
    param("Size < 256b", "DVD_PATH/VIDEO_TS/VIDEO_TS.BUP", 202, "\xca\x00\x00\x00"),
    param("Size < 64Kb", "DVD_PATH/VIDEO_TS/VIDEO_TS.IFO", 43051, "\x2b\xa8\x00\x00"),
    param("Size < 16Mb", "DVD_PATH/VIDEO_TS/VTS_01_1.VOB", 14412088, "\x38\xe9\xdb\x00"),
    param("Size < 4Gb", "DVD_PATH/VIDEO_TS/VTS_02_0.VOB", 3812800233, "\xe9\xb6\x42\xe3")
])
@patch("pydvdid.functions.getsize") # pylint: disable=locally-disabled, invalid-name
def _get_file_size_returns_correctly(description, file_path, file_size, expected, mock_getsize):
    """Tests that invocation of _get_file_size() returns correctly.
    """

    mock_getsize.return_value = file_size

    file_size_string = _get_file_size(file_path)

    template = "Test case '{0}' failed: expected '0x{1}', actual '0x{2}'."
    assert_message = template.format(description, hexlify(expected), hexlify(file_size_string))

    eq_(expected, file_size_string, assert_message)

    mock_getsize.assert_called_once_with(file_path)


#@istest
#@parameterized([
#    param(b"Standard DVD file", b"/VIDEO_TS/VIDEO_TS.IFO", b"VIDEO_TS.IFO", b"VIDEO_TS.IFO\x00"),
#    param(b"Filename with Unicode euro char", u"\u20ac.txt", u"\u20ac.txt", b"\xe2\x82\xac.txt\x00")
#])
#@patch("pydvdid.functions.basename") # pylint: disable=locally-disabled, invalid-name
#def _get_file_name_returns_correctly(description, file_path, file_name, expected, mock_basename):
#    """Tests that invocation of _get_file_name() returns correctly.
#    """
#
#    mock_basename.return_value = file_name
#
#    file_name_string = _get_file_name(file_path)
#
#    template = b"Test case '{0}' failed: expected '0x{1}', actual '0x{2}'."
#    assert_message = template.format(description, hexlify(expected), hexlify(file_name_string))
#
#    eq_(expected, file_name_string, assert_message)
#
#    mock_basename.assert_called_once_with(file_path)
