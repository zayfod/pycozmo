"""

AudioKinetic WWave exceptions.

"""

from .. import exception


__all__ = [
    "AudioKineticBaseError",
    "AudioKineticFormatError",
    "AudioKineticIOError",
]


class AudioKineticBaseError(exception.PyCozmoException):
    """ AudioKinetic WWise base error. """
    pass


class AudioKineticFormatError(AudioKineticBaseError):
    """ Invalid file format error. """
    pass


class AudioKineticIOError(AudioKineticBaseError):
    """ File I/O error. """
    pass
