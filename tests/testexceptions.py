"""Implements tests for the pydvdid.exceptions module.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from inspect import (
    getmembers, isclass
)
from mock import patch
from parameterized import (
    parameterized, param
)
from nose.tools import (
    eq_, istest, ok_
)
from pydvdid.exceptions import (
    FileContentReadException, FileTimeOutOfRangeException, PathDoesNotExistException,
    PydvdidException
)
import pydvdid


@istest
def pydvdidexception_is_not_instantiable(): # pylint: disable=locally-disabled, invalid-name
    """Tests that instantiation of PydvdidException raises an exception.
    """

    try:
        PydvdidException("This should not work.")
    except TypeError as expected:
        eq_("PydvdidException may not be directly instantiated.", str(expected))
    except Exception as unexpected: # pylint: disable=locally-disabled, broad-except
        ok_(False, "An unexpected {0} exception was raised.".format(type(unexpected).__name__))
    else:
        ok_(False, "An exception was expected but was not raised.")


@istest
@parameterized([
    param(7000, None, "No bytes are available."),
    param(20, 12, "20 bytes were expected, 12 were read.")
])
@patch("pydvdid.exceptions.PydvdidException.__init__") # pylint: disable=locally-disabled, invalid-name
def filecontentreadexception___init__calls_base___init___with_correct_message(expected_size,
                                                                              actual_size,
                                                                              expected_message,
                                                                              mock_init):
    """Tests that instantiation of FileContentReadException instantiates the base class with a
       formatted message.
    """

    mock_init.return_value = None

    FileContentReadException(expected_size, actual_size)

    mock_init.assert_called_once_with(expected_message)


@istest
@patch("pydvdid.exceptions.PydvdidException.__init__")
def filetimeoutofrangeexception___init__calls_base___init___with_correct_message(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Tests that instantiation of FileTimeOutOfRangeException instantiates the base class with a
       formatted message.
    """

    mock_init.return_value = None

    FileTimeOutOfRangeException(12345678)

    mock_init.assert_called_once_with("File Time '12345678' is outside of the allowable range.")


@istest
@patch("pydvdid.exceptions.PydvdidException.__init__")
def pathdoesnotexistexception___init__calls_base___init___with_correct_message(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Tests that instantiation of PathDoesNotExistException instantiates the base class with a
       formatted message.
    """

    mock_init.return_value = None

    PathDoesNotExistException("DVD_PATH")

    mock_init.assert_called_once_with("Path 'DVD_PATH' does not exist.")


@istest
def all_package_defined_exceptions_derive_from_pydvdidexception(): # pylint: disable=locally-disabled, invalid-name
    """Tests that all directly raisable exceptions defined in the pydvdid package (i.e. all except
       PydvdidException) are subclassed from PydvdidException.

       (This is a Nose generator test which discovers exceptions by inspection to ensure that all
       package defined exceptions are tested).
    """

    def _assert_exception_type_is_subclass_of_pydvdidexception(exception_type): # pylint: disable=locally-disabled, invalid-name, missing-docstring
        message = "{0} is not subclassed from PydvdidException.".format(exception_type.__name__)
        ok_(not issubclass(type, PydvdidException), message)

    for member_tuple in getmembers(pydvdid):
        member = member_tuple[1]

        if isclass(member) and issubclass(member, Exception) and member != PydvdidException:
            yield _assert_exception_type_is_subclass_of_pydvdidexception, member
