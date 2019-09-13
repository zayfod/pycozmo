
from abc import ABC, abstractmethod

from .protocol_declaration import PacketType
from .protocol_utils import BinaryReader, BinaryWriter
from .util import hex_dump


class Struct(ABC):

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def to_bytes(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def to_writer(self, writer: BinaryWriter) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_bytes(cls, buffer: bytes):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_reader(cls, reader: BinaryReader):
        raise NotImplementedError


class Packet(Struct, ABC):

    __slots__ = (
        "type",
        "seq",
        "ack",
    )

    def __init__(self, packet_type: PacketType):
        self.type = packet_type
        self.seq = 0
        self.ack = 0

    def is_oob(self) -> bool:
        res = self.type.value >= PacketType.EVENT.value
        return res


class UnknownPacket(Packet):

    __slots__ = (
        "_data",
    )

    def __init__(self, packet_type: PacketType, data: bytes):
        super().__init__(packet_type)
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = bytes(value)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return "{type_name}({type:02x}, {data})".format(
            type=self.type.value, type_name=type(self).__name__, data=hex_dump(data=self._data))

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()

    def to_writer(self, writer):
        writer.write_farray(self._data, "B", len(self._data))

    @classmethod
    def from_bytes(cls, buffer):
        # The size is not known.
        raise NotImplementedError

    @classmethod
    def from_reader(cls, reader):
        # The size is not known.
        raise NotImplementedError


class UnknownCommand(UnknownPacket):

    __slots__ = (
        "_ID",
    )

    def __init__(self, cmd_id: int, data: bytes = b""):
        super().__init__(PacketType.ACTION, data)
        self.ID = cmd_id

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = int(value)

    @classmethod
    def from_bytes(cls, buffer):
        # The size is not known.
        raise NotImplementedError

    @classmethod
    def from_reader(cls, reader):
        # The size is not known.
        raise NotImplementedError

    def __repr__(self):
        return "{type}({id:02x}, {data})".format(
            id=self._ID, type=type(self).__name__, data=hex_dump(data=self._data))


class UnknownEvent(UnknownPacket):

    __slots__ = (
        "_ID",
    )

    def __init__(self, cmd_id: int, data: bytes = b""):
        super().__init__(PacketType.EVENT, data)
        self.ID = cmd_id

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = int(value)

    @classmethod
    def from_bytes(cls, buffer):
        # The size is not known.
        raise NotImplementedError

    @classmethod
    def from_reader(cls, reader):
        # The size is not known.
        raise NotImplementedError

    def __repr__(self):
        return "{type}({id:02x}, {data})".format(
            id=self._ID, type=type(self).__name__, data=hex_dump(data=self._data))
