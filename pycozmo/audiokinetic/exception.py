"""

AudioKinetic WWave exceptions.

"""


class AudioKineticBaseError(Exception):
    """ AudioKinetic WWise base error. """
    pass


class AudioKineticFormatError(AudioKineticBaseError):
    """ Invalid file format error. """
    pass


class AudioKineticIOError(AudioKineticBaseError):
    """ File I/O error. """
