"""

Protocol AST declaration.

"""

from enum import Enum
from abc import ABC
from typing import List, Optional


FRAME_ID = b"COZ\x03RE\x01"
MIN_FRAME_SIZE = len(FRAME_ID) + 1 + 2 + 2 + 2


class FrameType(Enum):
    RESET = 1
    RESET_ACK = 2
    FIN = 3
    UNKNOWN_04 = 4
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


class Packet(ABC):
    """ Base class for packets. """

    def __init__(self, packet_id: PacketType, name: str, description: Optional[str] = None,
                 arguments: Optional[List[Argument]] = None):
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


class Unknown0A(Packet):

    def __init__(self):
        super().__init__(PacketType.UNKNOWN_0A, "unknown_0a")


class Protocol(object):
    """ Protocol declaration. """

    def __init__(self, packets: List[Packet]):
        self.packets = list(packets)


PROTOCOL = Protocol(packets=[
    Connect(),
    Disconnect(),
    Ping(),
    Unknown0A(),

    Command(0x32, "drive_wheels", arguments=[
        FloatArgument("lwheel_speed_mmps"),
        FloatArgument("rwheel_speed_mmps"),
        FloatArgument("lwheel_accel_mmps2"),
        FloatArgument("rwheel_accel_mmps2"),
    ]),
    Command(0x3b, "stop_all_motors"),
    Command(0x0b, "set_head_light", arguments=[
        BoolArgument("enable")
    ])
])
