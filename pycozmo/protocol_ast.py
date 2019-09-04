"""

Protocol AST.

"""

from enum import Enum
from abc import ABC
from typing import List, Optional, Union, Type


class FrameType(Enum):
    RESET = 1
    RESET_ACK = 2
    FIN = 3
    ENGINE_ACT = 4
    ENGINE = 7
    ROBOT = 9
    PING = 0x0b


class PacketType(Enum):
    UNKNOWN = -1
    CONNECT = 2
    DISCONNECT = 3
    ACTION = 4
    EVENT = 5
    UNKNOWN_0A = 0x0a
    PING = 0x0b


class Argument(ABC):
    """ Base class for packet arguments. """

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = str(name)
        self.description = str(description) if description else None


class FloatArgument(Argument):
    """ 32-bit floating point number. """

    def __init__(self, name: str, description: Optional[str] = None, default: float = 0.0):
        super().__init__(name, description)
        self.default = float(default)


class DoubleArgument(Argument):
    """ 64-bit floating point number. """

    def __init__(self, name: str, description: Optional[str] = None, default: float = 0.0):
        super().__init__(name, description)
        self.default = float(default)


class BoolArgument(Argument):
    """ 8-bit boolean. """

    def __init__(self, name: str, description: Optional[str] = None, default: bool = False):
        super().__init__(name, description)
        self.default = bool(default)


class UInt8Argument(Argument):
    """ 8-bit unsigned integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class UInt16Argument(Argument):
    """ 16-bit unsigned integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class UInt32Argument(Argument):
    """ 32-bit unsigned integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class Int8Argument(Argument):
    """ 8-bit signed integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class Int16Argument(Argument):
    """ 16-bit signed integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class Int32Argument(Argument):
    """ 32-bit signed integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class FArrayArgument(Argument):
    """ Fixed-length array. """

    def __init__(self, name: str, description: Optional[str] = None,
                 data_type: Union[Type[Argument], str] = UInt8Argument, length: int = 0, default=()):
        super().__init__(name, description)
        self.data_type = data_type
        self.length = length
        self.default = tuple(default)


class VArrayArgument(Argument):
    """ Variable-length array. """

    def __init__(self, name: str, description: Optional[str] = None,
                 data_type: Type[Argument] = UInt8Argument, length_type: Type[Argument] = UInt16Argument, default=()):
        super().__init__(name, description)
        self.data_type = data_type
        self.length_type = length_type
        self.default = tuple(default)


class StringArgument(Argument):
    """ String. """

    def __init__(self, name: str, description: Optional[str] = None,
                 length_type: Type[Argument] = UInt16Argument, default=""):
        super().__init__(name, description)
        self.length_type = length_type
        self.default = str(default)


class Struct(ABC):
    """ Base class for structures. """

    def __init__(self, name: str, description: Optional[str] = None,
                 arguments: Optional[List[Argument]] = None):
        self.name = str(name)
        self.description = str(description) if description else None
        self.arguments = list(arguments) if arguments else []


class Packet(Struct, ABC):
    """ Base class for packets. """

    def __init__(self, packet_id: PacketType, name: str, description: Optional[str] = None,
                 arguments: Optional[List[Argument]] = None):
        super().__init__(name, description, arguments)
        # TODO: Rename to "type".
        self.packet_id = PacketType(packet_id)
        self.name = str(name)
        self.description = str(description) if description else None
        self.arguments = list(arguments) if arguments else []


class Connect(Packet):
    """ Connection acknowledgement packet. """

    def __init__(self):
        super().__init__(PacketType.CONNECT, "connect")


class Disconnect(Packet):
    """ Disconnect packet. """

    def __init__(self):
        super().__init__(PacketType.DISCONNECT, "disconnect")


# TODO: Rename to "Action".
class Command(Packet):
    """ Command packet. """

    def __init__(self, cmd_id: int, name: str, description: Optional[str] = None,
                 arguments: Optional[List[Argument]] = None):
        super().__init__(PacketType.ACTION, name, description, arguments)
        self.id = int(cmd_id)


class Event(Packet):
    """ Event packet. """

    def __init__(self, evt_id: int, name: str, description: Optional[str] = None,
                 arguments: Optional[List[Argument]] = None):
        super().__init__(PacketType.EVENT, name, description, arguments)
        self.id = int(evt_id)


class Ping(Packet):
    """ Ping packet. """

    def __init__(self):
        super().__init__(PacketType.PING, "ping", arguments=[
            DoubleArgument("time_sent_ms"),
            UInt32Argument("counter"),
            UInt32Argument("last"),
            UInt8Argument("unknown"),
        ])


class Protocol(object):
    """ Protocol declaration. """

    def __init__(self, structs: List[Struct], packets: List[Packet]):
        self.structs = list(structs)
        self.packets = list(packets)
