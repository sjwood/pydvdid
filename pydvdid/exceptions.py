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


class DvdPathDoesNotExistException(PydvdidException):
    """Implements a class that represents the exception raised when a DVD path does not exist.
    """

    def __init__(self, dvd_path):
        template = "Path '{0}' does not exist."
        super(DvdPathDoesNotExistException, self).__init__(template.format(dvd_path))


class VideoTsPathDoesNotExistException(PydvdidException):
    """Implements a class that represents the exception raised when a DVD path does not contain a
       VIDEO_TS folder.
    """

    def __init__(self, video_ts_path):
        template = "Path '{0}' does not exist."
        super(VideoTsPathDoesNotExistException, self).__init__(template.format(video_ts_path))
