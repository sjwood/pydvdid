"""Implements tests for the pydvdid.functions module.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from binascii import hexlify
from mock import (
    call, MagicMock, patch
)
from nose_parameterized import (
    parameterized, param
)
from nose.tools import (
    eq_, istest, nottest, ok_
)
from sys import version_info
from pydvdid.exceptions import (
    FileContentReadException, FileTimeOutOfRangeException, PathDoesNotExistException
)
from pydvdid.functions import (
    _check_dvd_path_exists, _check_video_ts_path_exists, _get_file_creation_time, _get_file_name,
    _get_file_size, _get_first_64k_content, _get_video_ts_file_paths, _get_vmgi_file_content,
    _get_vts01i_file_content
)


@istest
@patch("pydvdid.functions.isdir")
def _check_dvd_path_exists_does_not_raise_exception_when_path_exists(mock_isdir): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _check_dvd_path_exists() with a valid path does not raise an
       exception.
    """

    mock_isdir.return_value = True

    try:
        _check_dvd_path_exists("DVD_PATH")
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(exception).__name__))

    mock_isdir.assert_called_once_with("DVD_PATH")


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
        _check_video_ts_path_exists("DVD_PATH")
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(exception).__name__))

    mock_isdir.assert_called_once_with("DVD_PATH/VIDEO_TS")


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
        "VTS_01_0.VOB", "unexpected_folder", "VTS_01_0.BUP", "VTS_01_0.IFO"
    ]

    mock_isfile.side_effect = [True, False, True, True]

    video_ts_file_paths = _get_video_ts_file_paths("DVD_PATH")

    eq_([
        "DVD_PATH/VIDEO_TS/VTS_01_0.BUP", "DVD_PATH/VIDEO_TS/VTS_01_0.IFO",
        "DVD_PATH/VIDEO_TS/VTS_01_0.VOB"
    ], video_ts_file_paths)

    mock_listdir.assert_called_once_with("DVD_PATH/VIDEO_TS")

    mock_isfile.assert_has_calls([
        call("DVD_PATH/VIDEO_TS/VTS_01_0.VOB"), call("DVD_PATH/VIDEO_TS/unexpected_folder"),
        call("DVD_PATH/VIDEO_TS/VTS_01_0.BUP"), call("DVD_PATH/VIDEO_TS/VTS_01_0.IFO")
    ])


@istest
@parameterized([
    param("Creation Time '1600-12-31 23:59:59'", "DVD_PATH/VIDEO_TS/VIDEO_TS.BUP", -11644473601),
    param("Creation Time '10000-01-01 00:00:00'", "DVD_PATH/VIDEO_TS/VIDEO_TS.IFO", 253402300800)
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
    param("Creation Time '1601-01-01 00:00:00'", "DVD_PATH/VIDEO_TS/VTS_02_0.IFO", -11644473600,
          bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])),
    param("Creation Time '9999-12-31 23:59:59'", "DVD_PATH/VIDEO_TS/VTS_02_1.VOB", 253402300799,
          bytearray([0x80, 0xa9, 0x27, 0xd1, 0x5e, 0x5a, 0xc8, 0x24])),
    param("Creation Time '2015-07-01 21:51:43'", "DVD_PATH/VIDEO_TS/VTS_02_2.VOB", 1435787503,
          bytearray([0x80, 0x01, 0x23, 0x1e, 0x48, 0xb4, 0xd0, 0x01]))
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

    file_creation_time_bytearray = _get_file_creation_time(file_path)

    template = "Test case {0}' failed: expected '{1}', actual '{2}'."
    assert_message = template.format(description, _format_as_bytestring(expected),
                                     _format_as_bytestring(file_creation_time_bytearray))

    eq_(expected, file_creation_time_bytearray, assert_message)

    mock_getctime.assert_called_once_with(file_path)


@istest
@parameterized([
    param("Size less than 256b", "DVD_PATH/VIDEO_TS/VIDEO_TS.BUP", 202,
          bytearray([0xca, 0x00, 0x00, 0x00])),
    param("Size less than 64Kb", "DVD_PATH/VIDEO_TS/VIDEO_TS.IFO", 43051,
          bytearray([0x2b, 0xa8, 0x00, 0x00])),
    param("Size less than 16Mb", "DVD_PATH/VIDEO_TS/VTS_01_1.VOB", 14412088,
          bytearray([0x38, 0xe9, 0xdb, 0x00])),
    param("Size less than 4Gb", "DVD_PATH/VIDEO_TS/VTS_02_0.VOB", 3812800233,
          bytearray([0xe9, 0xb6, 0x42, 0xe3]))
])
@patch("pydvdid.functions.getsize") # pylint: disable=locally-disabled, invalid-name
def _get_file_size_returns_correctly(description, file_path, file_size, expected, mock_getsize):
    """Tests that invocation of _get_file_size() returns correctly.
    """

    mock_getsize.return_value = file_size

    file_size_bytearray = _get_file_size(file_path)

    template = "Test case '{0}' failed: expected '{1}', actual '{2}'."
    assert_message = template.format(description, _format_as_bytestring(expected),
                                     _format_as_bytestring(file_size_bytearray))

    eq_(expected, file_size_bytearray, assert_message)

    mock_getsize.assert_called_once_with(file_path)


@istest
@parameterized([
    param("Filename with Unicode euro char", "/VIDEO_TS/1\u20ac.txt", "1\u20ac.txt",
          bytearray([0x31, 0xe2, 0x82, 0xac, 0x2e, 0x74, 0x78, 0x74, 0x00])),
    param("Standard DVD file", "/VIDEO_TS/VIDEO_TS.IFO", "VIDEO_TS.IFO",
          bytearray([0x56, 0x49, 0x44, 0x45, 0x4f, 0x5f, 0x54, 0x53, 0x2e, 0x49, 0x46, 0x4f, 0x00]))
])
@patch("pydvdid.functions.basename") # pylint: disable=locally-disabled, invalid-name
def _get_file_name_returns_correctly(description, file_path, file_name, expected, mock_basename):
    """Tests that invocation of _get_file_name() returns correctly.
    """

    mock_basename.return_value = file_name

    file_name_bytearray = _get_file_name(file_path)

    template = "Test case '{0}' failed: expected '{1}', actual '{2}'."
    assert_message = template.format(description, _format_as_bytestring(expected),
                                     _format_as_bytestring(file_name_bytearray))

    eq_(expected, file_name_bytearray, assert_message)

    mock_basename.assert_called_once_with(file_path)


@istest
@patch("pydvdid.functions._get_first_64k_content")
def _get_vmgi_file_content_calls_through_to__get_first_64k_content(mock_get_first_64k_content): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _get_vmgi_file_content() calls a 'private' method to get the first
       65536 bytes of the specified file.
    """

    mock_get_first_64k_content.return_value = bytearray([0xa7, 0x20, 0x38, 0x1f, 0xaa])

    vmgi_file_content = _get_vmgi_file_content("DVD_PATH")

    eq_(bytearray([0xa7, 0x20, 0x38, 0x1f, 0xaa]), vmgi_file_content)

    mock_get_first_64k_content.assert_called_once_with("DVD_PATH/VIDEO_TS/VIDEO_TS.IFO")


@istest
@patch("pydvdid.functions._get_first_64k_content")
def _get_vts01i_file_content_calls_through_to__get_first_64k_content(mock_get_first_64k_content): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _get_vts01i_file_content() calls a 'private' method to get the first
       65536 bytes of the specified file.
    """

    mock_get_first_64k_content.return_value = bytearray([0x10, 0x31, 0x44, 0x0c])

    vts01i_file_content = _get_vts01i_file_content("DVD_PATH")

    eq_(bytearray([0x10, 0x31, 0x44, 0x0c]), vts01i_file_content)

    mock_get_first_64k_content.assert_called_once_with("DVD_PATH/VIDEO_TS/VTS_01_0.IFO")


@istest
@patch("pydvdid.functions.isfile")
def _get_first_64k_content_raises_exception_when_path_does_not_exist(mock_isfile): # pylint: disable=locally-disabled, invalid-name
    """Tests that invocation of _get_first_64k_content() with an invalid path raises a
       PathDoesNotExistException exception.
    """

    mock_isfile.return_value = False

    try:
        _get_first_64k_content("DVD_PATH/VIDEO_TS/VTS_99_0.IFO")
    except PathDoesNotExistException:
        pass
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(exception).__name__))
    else:
        ok_(False, "An exception was expected but was not raised.")

    mock_isfile.assert_called_once_with("DVD_PATH/VIDEO_TS/VTS_99_0.IFO")


@istest
@parameterized([
    param("DVD_PATH/VIDEO_TS/VTS_07_0.IFO", 5, None),
    param("DVD_PATH/VIDEO_TS/VTS_02_0.IFO", 8, 4)
])
@patch(("__builtin__" if version_info[0] < 3 else "builtins") + ".open")
@patch("pydvdid.functions.getsize")
@patch("pydvdid.functions.isfile") # pylint: disable=locally-disabled, invalid-name, too-many-arguments
def _get_first_64k_content_raises_exception_when_readinto_returns_insufficient_bytes(file_name,
                                                                                     file_size,
                                                                                     read_size,
                                                                                     mock_isfile,
                                                                                     mock_getsize,
                                                                                     mock_open):
    """Tests that invocation of _get_first_64k_content() raises a FileContentReadException when the
       number of bytes requested to be read from an existent file specified by the supplied file
       path cannot be read.
    """

    mock_isfile.return_value = True
    mock_getsize.return_value = file_size
    mock_file_object = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file_object
    mock_file_object.readinto.return_value = read_size

    try:
        _get_first_64k_content(file_name)
    except FileContentReadException:
        pass
    except Exception as exception: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(exception).__name__))
    else:
        ok_(False, "An exception was expected but was not raised.")

    mock_isfile.assert_called_once_with(file_name)
    mock_getsize.assert_called_once_with(file_name)
    mock_open.assert_called_once_with(file_name, "rb")
    mock_file_object.readinto.assert_called_once_with(bytearray(file_size))


@istest
@patch(("__builtin__" if version_info[0] < 3 else "builtins") + ".open")
@patch("pydvdid.functions.getsize")
@patch("pydvdid.functions.isfile")
def _get_first_64k_content_returns_correctly_when_file_content_less_than_64k(mock_isfile, # pylint: disable=locally-disabled, invalid-name
                                                                             mock_getsize,
                                                                             mock_open):
    """Tests that invocation of _get_first_64k_content() returns the entire file content as a
       bytearray for an existent file which is less than 64Kb in size.
    """

    mock_isfile.return_value = True
    mock_getsize.return_value = 10
    mock_file_object = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file_object
    expected_file_content = bytearray([0x43, 0x90, 0xdc, 0x18, 0xf4, 0xee, 0x25, 0x51, 0xb7, 0xa3])
    def _fake_readinto(byte_array): # pylint: disable=locally-disabled, missing-docstring
        for index in range(0, len(byte_array)):
            byte_array[index] = expected_file_content[index]
        return len(byte_array)
    mock_file_object.readinto.side_effect = _fake_readinto

    first_64k_content = _get_first_64k_content("DVD_PATH/VIDEO_TS/VIDEO_TS.IFO")
    eq_(expected_file_content, first_64k_content)

    mock_isfile.assert_called_once_with("DVD_PATH/VIDEO_TS/VIDEO_TS.IFO")
    mock_getsize.assert_called_once_with("DVD_PATH/VIDEO_TS/VIDEO_TS.IFO")
    mock_open.assert_called_once_with("DVD_PATH/VIDEO_TS/VIDEO_TS.IFO", "rb")
    mock_file_object.readinto.assert_called_once_with(expected_file_content)


@istest
@patch(("__builtin__" if version_info[0] < 3 else "builtins") + ".open")
@patch("pydvdid.functions.getsize")
@patch("pydvdid.functions.isfile")
def _get_first_64k_content_returns_correctly_when_file_content_greater_than_64k(mock_isfile, # pylint: disable=locally-disabled, invalid-name
                                                                                mock_getsize,
                                                                                mock_open):
    """Tests that invocation of _get_first_64k_content() returns the first 64Kb of content as a
       bytearray for an existent file which is greater than 64Kb in size.
    """

    mock_isfile.return_value = True
    mock_getsize.return_value = 100000
    mock_file_object = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file_object
    expected_file_content = bytearray(100000)
    for index in range(0, len(expected_file_content)):
        expected_file_content[index] = index & 0xff
    def _fake_readinto(byte_array): # pylint: disable=locally-disabled, missing-docstring
        for index in range(0, len(byte_array)):
            byte_array[index] = expected_file_content[index]
        return len(byte_array)
    mock_file_object.readinto.side_effect = _fake_readinto

    first_64k_content = _get_first_64k_content("DVD_PATH/VIDEO_TS/VIDEO_TS.BUP")
    eq_(expected_file_content[:65536], first_64k_content)

    mock_isfile.assert_called_once_with("DVD_PATH/VIDEO_TS/VIDEO_TS.BUP")
    mock_getsize.assert_called_once_with("DVD_PATH/VIDEO_TS/VIDEO_TS.BUP")
    mock_open.assert_called_once_with("DVD_PATH/VIDEO_TS/VIDEO_TS.BUP", "rb")
    mock_file_object.readinto.assert_called_once_with(expected_file_content[:65536])


@nottest
def _format_as_bytestring(value):
    """Simple utility function for providing a hex representation of a unicode string, compatible
       with both Python2 and Python3.
    """

    return "0x" + str(hexlify(bytes(value))).replace("b'", "").replace("'", "")
