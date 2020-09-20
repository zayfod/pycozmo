"""

Exceptions declaration.

"""

__all__ = [
    "PyCozmoException",
    "PyCozmoConnectionError",
    "ConnectionTimeout",
    "UnsupportedFirmwareVersion",
    "Timeout",
]


class PyCozmoException(Exception):
    """ Base class for all PyCozmo exceptions. """


class PyCozmoConnectionError(PyCozmoException):
    """ Base class for all PyCozmo connection exceptions. """


class ConnectionTimeout(PyCozmoConnectionError):
    """ Connection timeout. """


class UnsupportedFirmwareVersion(PyCozmoConnectionError):
    """ Unsupported Cozmo firmware version. """


class Timeout(PyCozmoException):
    """ Timeout. """
