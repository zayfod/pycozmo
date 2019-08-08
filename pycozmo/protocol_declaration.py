"""

Protocol AST declaration.

"""

from abc import ABC
from typing import List, Optional


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


class BoolArgument(Argument):
    """ 8-bit boolean. """

    def __init__(self, name: str, description: Optional[str] = None, default: bool = False):
        super().__init__(name, description)
        self.default = bool(default)


class Packet(ABC):
    """ Base class for packets. """

    def __init__(self, packet_id: int, name: str, description: Optional[str] = None,
                 arguments: Optional[List[Argument]] = None):
        self.packet_id = int(packet_id)
        self.name = str(name)
        self.description = str(description) if description else None
        self.arguments = list(arguments) if arguments else []


class Connect(Packet):
    """ Connection acknowledgement packet. """

    def __init__(self):
        super().__init__(2, "connect")


class Disconnect(Packet):
    """ Disconnect packet. """

    def __init__(self):
        super().__init__(3, "disconnect")


class Command(Packet):
    """ Command packet. """

    def __init__(self, cmd_id: int, name: str, description: Optional[str] = None,
                 arguments: Optional[List[Argument]] = None):
        super().__init__(4, name, description, arguments)
        self.id = int(cmd_id)


class Event(Packet):
    """ Event packet. """

    def __init__(self, evt_id: int, name: str, description: Optional[str] = None,
                 arguments: Optional[List[Argument]] = None):
        super().__init__(5, name, description, arguments)
        self.id = int(evt_id)


class Protocol(object):
    """ Protocol declaration. """

    def __init__(self, packets: List[Packet]):
        self.packets = list(packets)


PROTOCOL = Protocol(
    packets=[
        Connect(),
        Disconnect(),

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
