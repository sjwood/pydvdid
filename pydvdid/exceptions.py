"""Implements all pydvdid package-specific exceptions.
"""


from __future__ import unicode_literals


class PydvdidException(Exception):
    """Implements a class that represents an exception raised by the pydvdid package. This exception
       is never directly raised and is intended to be used in an 'except' block to handle any
       exception that originates from the package.
    """

    def __new__(cls, *args, **kwargs):
        if cls is PydvdidException:
            raise TypeError("PydvdidException may not be directly instantiated.")

        return Exception.__new__(cls, *args, **kwargs)


class FileContentReadException(PydvdidException):
    """Implements a class that represents the exception raised when a file's content cannot be
       successfully read.
    """

    def __init__(self, expected_size, actual_size):
        if actual_size is None:
            template = "No bytes are available."
        else:
            template = "{0} bytes were expected, {1} were read."

        super(FileContentReadException, self).__init__(template.format(expected_size, actual_size))


class FileTimeOutOfRangeException(PydvdidException):
    """Implements a class that represents the exception raised when a file's creation or
       modification time is outside the allowable range (i.e. before 1601-01-01 00:00:00 or after
       9999-12-31 23:59:59).
    """

    def __init__(self, file_time):
        template = "File Time '{0}' is outside of the allowable range."
        super(FileTimeOutOfRangeException, self).__init__(template.format(file_time))


class PathDoesNotExistException(PydvdidException):
    """Implements a class that represents the exception raised when a path does not exist.
    """

    def __init__(self, path):
        template = "Path '{0}' does not exist."
        super(PathDoesNotExistException, self).__init__(template.format(path))
