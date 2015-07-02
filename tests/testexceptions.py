"""Implements tests for the pydvdid.exceptions module.
"""


from __future__ import absolute_import
from inspect import getmembers, isclass
from mock import patch
from nose.tools import eq_, istest, nottest, ok_
from pydvdid import (
    FileTimeOutOfRangeException,
    PathDoesNotExistException,
    PydvdidException
)
import pydvdid


@istest
def pydvdidexception_is_not_instantiable(): # pylint: disable=locally-disabled, invalid-name
    """Tests that instantiation of PydvdidException raises an exception.
    """

    try:
        PydvdidException(b"This should not work.")
    except TypeError as expected:
        eq_(b"PydvdidException may not be directly instantiated.", str(expected))
    except Exception as unexpected: # pylint: disable=locally-disabled, broad-except
        ok_(False, b"An unexpected {0} exception was raised.".format(type(unexpected).__name__))
    else:
        ok_(False, b"An exception was expected but was not raised.")


@istest
@patch(b"pydvdid.exceptions.PydvdidException.__init__")
def pathdoesnotexistexception___init__calls_base___init___with_correct_message(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Tests that instantiation of PathDoesNotExistException instantiates the base class with a
       formatted message.
    """

    mock_init.return_value = None

    PathDoesNotExistException(b"DVD_PATH")

    mock_init.assert_called_once_with(b"Path 'DVD_PATH' does not exist.")


@istest
@patch(b"pydvdid.exceptions.PydvdidException.__init__")
def filetimeoutofrangeexception___init__calls_base___init___with_correct_message(mock_init): # pylint: disable=locally-disabled, invalid-name
    """Tests that instantiation of FileTimeOutOfRangeException instantiates the base class with a
       formatted message.
    """

    mock_init.return_value = None

    FileTimeOutOfRangeException(12345678)

    mock_init.assert_called_once_with(b"File Time '12345678' is outside of the allowable range.")


@istest
def all_package_defined_exceptions_derive_from_pydvdidexception(): # pylint: disable=locally-disabled, invalid-name
    """Tests that all directly raisable exceptions defined in the pydvdid package (i.e. all except
       PydvdidException) are subclassed from PydvdidException.

       (This is a Nose generator test which discovers exceptions by inspection to ensure that all
       package defined exceptions are tested).
    """

    for member_tuple in getmembers(pydvdid):
        member = member_tuple[1]

        if isclass(member) and issubclass(member, Exception) and member != PydvdidException:
            yield _assert_exception_type_is_subclass_of_pydvdidexception, member


@nottest
def _assert_exception_type_is_subclass_of_pydvdidexception(exception_type): # pylint: disable=locally-disabled, invalid-name
    """Asserts that supplied exception type is a subclass of PydvdidException.
    """

    assert_message = b"{0} is not subclassed from PydvdidException.".format(exception_type.__name__)

    ok_(not issubclass(type, PydvdidException), assert_message)
