"""

Cozmo protocol encoding helper classes and functions.

"""

from typing import Dict, Tuple
import struct


__all__ = [
    "validate_float",
    "validate_bool",
    "validate_integer",
    "validate_object",
    "validate_farray",
    "validate_varray",
    "validate_string",

    "get_size",
    "get_farray_size",
    "get_varray_size",
    "get_string_size",
    "get_object_size",
    "get_object_farray_size",

    "BinaryReader",
    "BinaryWriter",
]


_struct_cache = dict()  # type: Dict[Tuple[str, int], struct.Struct]


def _get_struct(fmt: str, length: int) -> struct.Struct:
    key = (fmt, length)
    if key in _struct_cache:
        return _struct_cache[key]
    else:
        reader = struct.Struct("<{0}{1}".format(length, fmt))
        _struct_cache[key] = reader
        return reader


def validate_float(name, value):
    try:
        value = float(value)
    except ValueError:
        raise ValueError("{name} must be float. Got {type}.".format(name=name, type=type(value).__name__))
    return value


def validate_bool(name, value):
    try:
        value = bool(value)
    except ValueError:
        raise ValueError("{name} must be bool. Got {type}.".format(name=name, type=type(value).__name__))
    return value


def validate_integer(name, value, minimum, maximum):
    try:
        value = int(value)
    except ValueError:
        raise ValueError("{name} must be an integer. Got a {type}.".format(name=name, type=type(value).__name__))
    if value < minimum or value > maximum:
        raise ValueError("{name} must be between {minimum} and {maximum}. Got {value}.".format(
            name=name, minimum=minimum, maximum=maximum, value=value))
    return value


def validate_object(name, value, expected_type):
    if not isinstance(value, expected_type):
        raise ValueError("{name} must be a {expected_type}. Got a {value_type}.".format(
            name=name, expected_type=expected_type.__name__, value_type=type(value).__name__))
    return value


def validate_farray(name, value, length, element_validation):
    try:
        value = tuple(value)
    except ValueError:
        raise ValueError("{name} must be a sequence. Got a {type}.".format(name=name, type=type(value).__name__))
    if len(value) != length:
        raise ValueError(("{name} must be a sequence of length {expected_length}. "
                          "Got a sequence of length {value_length}.").format(
            name=name, expected_length=length, value_length=len(value)))
    return [element_validation((name, i), element) for i, element in enumerate(value)]


def validate_varray(name, value, maximum_length, element_validation):
    try:
        value = tuple(value)
    except ValueError:
        raise ValueError("{name} must be a sequence. Got a {type}.".format(name=name, type=type(value).__name__))
    if len(value) > maximum_length:
        raise ValueError(("{name} must be a sequence with length less than or equal to {maximum_length}. "
                          "Got a sequence of length {value_length}.").format(
            name=name, maximum_length=maximum_length, value_length=len(value)))
    return [element_validation((name, i), element) for i, element in enumerate(value)]


def validate_string(name, value, maximum_length):
    if len(value) > maximum_length:
        raise ValueError(("{name} must be a string with less than or equal to {maximum_length}. "
                          "Got a string of length {value_length}.").format(
            name=name, maximum_length=maximum_length, value_length=len(value)))
    return value


def get_size(fmt):
    """ Figures out the size of a value with the given format. """
    return _get_struct(fmt, 1).size


def get_farray_size(fmt, length):
    """ Figures out the size of a fixed array with given format. """
    return _get_struct(fmt, length).size


def get_varray_size(value, length_format, data_format):
    """ Figures out the size of a variable-length array with given format. """
    return _get_struct(length_format, 1).size + _get_struct(data_format, len(value)).size


def get_string_size(value, length_format):
    """ Figures out the size of a string with given length format. """
    buf = value.encode('utf_8')
    return _get_struct(length_format, 1).size + _get_struct('s', len(buf)).size


def get_object_size(value):
    """ Figures out the size of a given object. """
    return len(value)


def get_object_farray_size(value, length):
    """ Figures out the size of a given fixed-length object sequence. """
    if len(value) != length:
        raise ValueError("The given fixed-length sequence has the wrong length.")
    if not value:
        return 0
    else:
        return sum(get_object_size(element) for element in value)


class BinaryReader(object):
    """ Used to read in a stream of binary data, keeping track of the current position. """

    def __init__(self, buffer: bytes, offset: int = 0):
        self._buffer = buffer
        self._index = offset

    @property
    def buffer(self):
        return self._buffer

    def __len__(self):
        return len(self._buffer)

    def seek_set(self, offset: int) -> None:
        if offset < 0 or offset > len(self._buffer):
            ValueError("Invalid offset.")
        self._index = offset

    def seek_cur(self, offset: int) -> None:
        offset += self._index
        if offset < 0 or offset > len(self._buffer):
            ValueError("Invalid offset.")
        self._index = offset

    def tell(self):
        """ Returns the current stream position as an offset within the buffer. """
        return self._index

    def read(self, fmt):
        """ Reads in a single value of the given format. """
        return self.read_farray(fmt, 1)[0]

    def read_farray(self, fmt, length):
        """ Reads in a fixed-length array of the given format and length. """
        reader = _get_struct(fmt, length)
        if self._index + reader.size > len(self._buffer):
            raise IndexError('Buffer not large enough to read serialized message. Received {0} bytes.'.format(
                len(self._buffer)))
        result = reader.unpack_from(self._buffer, self._index)
        self._index += reader.size
        return result

    def read_varray(self, data_format, length_format):
        """ Reads in a variable-length array with the given length format and data format. """
        length = self.read(length_format)
        return self.read_farray(data_format, length)

    def read_string(self, length_format):
        """ Reads in a variable-length string with the given length format. """
        length = self.read(length_format)
        bs = self.read_farray('s', length)[0]
        return bs.decode('utf_8')

    def read_string_farray(self, string_length_format, array_length):
        """ Reads in a fixed-length array of variable-length strings with the given length format. """
        return [self.read_string(string_length_format) for _ in range(array_length)]

    def read_string_varray(self, string_length_format, array_length_format):
        """ Reads in a variable-length array of variable-length strings with the given length format. """
        array_length = self.read(array_length_format)
        return [self.read_string(string_length_format) for _ in range(array_length)]

    def read_object(self, from__reader_method):
        """ Reads in an object according to the given method. """
        return from__reader_method(self)

    def read_object_farray(self, from__reader_method, length):
        """ Reads in a fixed-length object sequence according to the given method. """
        return [from__reader_method(self) for _ in range(length)]

    def read_object_varray(self, from__reader_method, length_format):
        """ Reads in a variable-length object sequence according to the given method. """
        length = self.read(length_format)
        return [from__reader_method(self) for _ in range(length)]


class BinaryWriter(object):
    """ Used to write out a stream of binary data. """

    def __init__(self):
        self._buffer = []

    def __len__(self):
        return len(self._buffer)

    def clear(self):
        del self._buffer[:]

    def dumps(self) -> bytes:
        return b"".join(self._buffer)

    def write_bytes(self, value: bytes) -> None:
        """ Writes out a byte sequence. """
        self._buffer.append(value)

    def write(self, value, fmt):
        """ Writes out a single value of the given format. """
        self.write_farray((value,), fmt, 1)

    def write_farray(self, value, fmt, length):
        """ Writes out a fixed-length array of the given format and length. """
        writer = _get_struct(fmt, length)
        self._buffer.append(writer.pack(*value))

    def write_varray(self, value, data_format, length_format):
        """ Writes out a variable-length array with the given length format and data format. """
        self.write(len(value), length_format)
        self.write_farray(value, data_format, len(value))

    def write_string(self, value, length_format):
        """ Writes out a variable-length string with the given length format. """
        bs = value.encode('utf_8')
        self.write(len(bs), length_format)
        self.write_farray((bs,), 's', len(bs))

    def write_string_farray(self, value, string_length_format, array_length):
        """ Writes out a fixed-length array of variable-length strings with the given length format. """
        if len(value) != array_length:
            raise ValueError('The given fixed-length sequence has the wrong length.')
        for element in value:
            self.write_string(element, string_length_format)

    def write_string_varray(self, value, string_length_format, array_length_format):
        """ Writes out a variable-length array of variable-length strings with the given length format. """
        self.write(len(value), array_length_format)
        for element in value:
            self.write_string(element, string_length_format)

    def write_object(self, value):
        """ Writes out an object that supports a to_writer() method. """
        value.to_writer(self)

    def write_object_farray(self, value, length):
        """ Writes out a fixed-length object sequence that supports a to_writer() method. """
        if len(value) != length:
            raise ValueError('The given fixed-length sequence has the wrong length.')
        for element in value:
            element.to_writer(self)

    def write_object_varray(self, value, length_format):
        """ Writes out a variable-length object sequence that supports a to_writer() method. """
        self.write(len(value), length_format)
        for element in value:
            element.to_writer(self)
