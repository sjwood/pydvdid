"""Implements all pydvdid package-specific exceptions.
"""


class PydvdidException(Exception):
    """Implements a class that represents an exception raised by the pydvdid package. This exception
       is never directly raised and is intended to be used in an 'except' block to handle any
       exception that originates from the package.
    """

    def __new__(cls, *args, **kwargs):
        if cls is PydvdidException:
            raise TypeError("PydvdidException may not be directly instantiated.")

        return Exception.__new__(cls, *args, **kwargs)


class PathDoesNotExistException(PydvdidException):
    """Implements a class that represents the exception raised when a path does not exist.
    """

    def __init__(self, path):
        template = "Path '{0}' does not exist."
        super(PathDoesNotExistException, self).__init__(template.format(path))


class FileTimeOutOfRangeException(PydvdidException):
    """Implements a class that represents the exception raised when a file's creation or
       modification time is outside the allowable range (i.e. before 1601-01-01 00:00:00 or after
       9999-12-31 23:59:59).
    """

    def __init__(self, file_time):
        template = "File Time '{0}' is outside of the allowable range."
        message = template.format(file_time)
        super(FileTimeOutOfRangeException, self).__init__(message)
