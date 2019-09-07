"""

Protocol AST.

"""

import enum
from abc import ABC
from typing import List, Optional, Union, Type


class FrameType(enum.Enum):
    RESET = 1
    RESET_ACK = 2
    FIN = 3
    ENGINE_ACT = 4
    ENGINE = 7
    ROBOT = 9
    PING = 0x0b


class PacketType(enum.Enum):
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


class UIntArgument(Argument, ABC):
    """ Base class for unsigned integers. """


class UInt8Argument(UIntArgument):
    """ 8-bit unsigned integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class UInt16Argument(UIntArgument):
    """ 16-bit unsigned integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class UInt32Argument(UIntArgument):
    """ 32-bit unsigned integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class IntArgument(Argument, ABC):
    """ Base class for signed integers. """


class Int8Argument(IntArgument):
    """ 8-bit signed integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class Int16Argument(IntArgument):
    """ 16-bit signed integer. """

    def __init__(self, name: str, description: Optional[str] = None, default: int = 0):
        super().__init__(name, description)
        self.default = int(default)


class Int32Argument(IntArgument):
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


class EnumMember(object):
    """ Base class for enumeration members. """

    def __init__(self, name: str, value: int, description: Optional[str] = None):
        self.name = str(name)
        self.description = str(description) if description else None
        self.value = int(value)


class Enum(object):
    """ Base class for enumerations. """

    def __init__(self, name: str, description: Optional[str] = None,
                 members: Optional[List[EnumMember]] = None):
        self.name = str(name)
        self.description = str(description) if description else None
        self.members = list(members) if members else []


class EnumArgument(Argument):
    """ Base class for enumeration arguments. """

    def __init__(self, name: str, enum_type: Enum, description: Optional[str] = None,
                 data_type: Union[Type[IntArgument], Type[UIntArgument]] = Int8Argument,
                 default=0):
        super().__init__(name, description)
        self.enum_type = enum_type
        self.data_type = data_type
        self.default = default


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


class Unknown0A(Packet):

    def __init__(self):
        super().__init__(PacketType.UNKNOWN_0A, "Unknown0A")


class Protocol(object):
    """ Protocol declaration. """

    def __init__(self, enums: List[Enum], structs: List[Struct], packets: List[Packet]):
        self.enums = list(enums)
        self.structs = list(structs)
        self.packets = list(packets)
