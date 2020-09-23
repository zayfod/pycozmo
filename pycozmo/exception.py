"""

Exceptions declaration.

"""

__all__ = [
    "PyCozmoException",
    "PyCozmoConnectionError",
    "ConnectionTimeout",
    "Timeout",
]


class PyCozmoException(Exception):
    """ Base class for all PyCozmo exceptions. """


class PyCozmoConnectionError(PyCozmoException):
    """ Base class for all PyCozmo connection exceptions. """


class ConnectionTimeout(PyCozmoConnectionError):
    """ Connection timeout. """


class Timeout(PyCozmoException):
    """ Timeout. """
