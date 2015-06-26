"""Implements the TestExceptions class.
"""


from __future__ import absolute_import
from inspect import getmembers, isclass
from unittest import TestCase
from pydvdid import PydvdidException
import pydvdid


class TestExceptions(TestCase):
    """Implements a class that contains tests for the pydvdid.exceptions module.
    """

    def test_pydvdidexception_is_not_instantiable(self): # pylint: disable=locally-disabled, invalid-name
        """Test that instantiation of PydvdidException raises an exception.
        """

        with self.assertRaises(TypeError) as context_manager:
            PydvdidException("This should not work.")

        message = context_manager.exception.message
        self.assertEqual("PydvdidException may not be directly instantiated.", message)


    def test_all_package_defined_exceptions_derive_from_pydvdidexception(self): # pylint: disable=locally-disabled, invalid-name
        """Test that all directly raisable exceptions defined in the pydvdid package (i.e. all
           except PydvdidException) are subclassed from PydvdidException.
        """

        # discover (by inspection) all raisable exceptions defined in the pydvdid package
        all_members = [t[1] for t in getmembers(pydvdid)]
        all_exceptions = [m for m in all_members if isclass(m) and issubclass(m, Exception)]
        raisable_exceptions = [e for e in all_exceptions if e != PydvdidException]

        incorrectly_defined_exceptions = []

        for raisable_exception in raisable_exceptions:
            if not issubclass(raisable_exception, PydvdidException):
                incorrectly_defined_exceptions.append(raisable_exception.__name__)

        if len(incorrectly_defined_exceptions) > 0:
            template = "Exception{0} {1} {2} not subclassed from PydvdidException."
            plural_or_singular = "s" if len(incorrectly_defined_exceptions) > 1 else ""
            exceptions_string = ", ".join(incorrectly_defined_exceptions)
            are_or_is = "are" if len(incorrectly_defined_exceptions) > 1 else "is"
            message = template.format(plural_or_singular, exceptions_string, are_or_is)
            self.fail(message)
