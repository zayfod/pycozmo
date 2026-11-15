"""

Minimal IFF/RIFF-style chunk reader.

Replacement for the standard library chunk module, which was removed in Python 3.13 (PEP 594). Only little-endian,
non-aligned chunks, as used by AudioKinetic WWise SoundBank files, are supported.

"""

from typing import BinaryIO
import struct


__all__ = [
    "Chunk",
]


class Chunk:
    """ Little-endian, non-aligned chunk reader with an interface compatible with the former chunk.Chunk class. """

    def __init__(self, f: BinaryIO) -> None:
        self.file = f
        name = f.read(4)
        if len(name) < 4:
            raise EOFError
        size_data = f.read(4)
        if len(size_data) < 4:
            raise EOFError
        self.name: bytes = name
        self.size: int = struct.unpack("<L", size_data)[0]
        self.offset: int = f.tell()
        self.size_read = 0

    def getname(self) -> bytes:
        """ Return the name (ID) of the chunk. """
        return self.name

    def getsize(self) -> int:
        """ Return the size of the chunk data, excluding the header. """
        return self.size

    def read(self, size: int = -1) -> bytes:
        """ Read at most size bytes from the chunk. Read until the end of the chunk if size is negative. """
        remaining = self.size - self.size_read
        if size < 0 or size > remaining:
            size = remaining
        if size == 0:
            return b""
        data = self.file.read(size)
        self.size_read += len(data)
        return data

    def skip(self) -> None:
        """ Skip to the end of the chunk. """
        remaining = self.size - self.size_read
        if remaining <= 0:
            return
        try:
            self.file.seek(self.offset + self.size)
            self.size_read = self.size
        except OSError:
            while self.size_read < self.size:
                data = self.read(min(8192, self.size - self.size_read))
                if not data:
                    raise EOFError
