"""

Cozmo protocol implementation base.

"""

from typing import Optional
from abc import ABC, abstractmethod

from .protocol_ast import PacketType
from .protocol_declaration import FIRST_ROBOT_PACKET_ID
from .protocol_utils import BinaryReader, BinaryWriter
from .util import hex_dump


__all__ = [
    "Struct",
    "Packet",
    "UnknownPacket",
    "UnknownCommand",
    "UnknownEvent",
]


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
    def from_bytes(cls, buffer: bytes) -> "Struct":
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_reader(cls, reader: BinaryReader) -> "Struct":
        raise NotImplementedError


class Packet(Struct, ABC):

    __slots__ = (
        "_type",
        "_id",
        "seq",
        "ack",
    )

    def __init__(self, packet_type: PacketType, packet_id: Optional[int] = None):
        self.type = packet_type
        self.id = packet_id
        self.seq = 0
        self.ack = 0

    @property
    def type(self) -> PacketType:
        return self._type

    @type.setter
    def type(self, value: PacketType) -> None:
        self._type = PacketType(value)

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        self._id = value

    def is_oob(self) -> bool:
        res = self.type.value >= PacketType.EVENT.value     # type: bool
        return res

    def is_from_robot(self) -> bool:
        if self.id is not None:
            res = self.id >= FIRST_ROBOT_PACKET_ID
        else:
            res = self.type == PacketType.CONNECT or (self.type == PacketType.PING and self.seq > 0)
        return res

    def is_from_engine(self) -> bool:
        return not self.is_from_robot()


class UnknownPacket(Packet):

    __slots__ = (
        "_data",
    )

    def __init__(self, packet_type: PacketType, data: bytes, packet_id: Optional[int] = None):
        super().__init__(packet_type, packet_id)
        self.data = data

    @property
    def data(self) -> bytes:
        return self._data

    @data.setter
    def data(self, value: bytes) -> None:
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

    def __init__(self, packet_id: int, data: bytes = b""):
        super().__init__(PacketType.COMMAND, data, packet_id=packet_id)

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
            id=self.id, type=type(self).__name__, data=hex_dump(data=self._data))


class UnknownEvent(UnknownPacket):

    def __init__(self, packet_id: int, data: bytes = b""):
        super().__init__(PacketType.EVENT, data, packet_id=packet_id)

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
            id=self.id, type=type(self).__name__, data=hex_dump(data=self._data))
