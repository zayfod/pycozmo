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
                 data_type: Argument = UInt8Argument, length: int = 0, default=()):
        super().__init__(name, description)
        self.data_type = data_type
        self.length = length
        self.default = tuple(default)


class VArrayArgument(Argument):
    """ Variable-length array. """

    def __init__(self, name: str, description: Optional[str] = None,
                 data_type: Argument = UInt8Argument, length_type: Argument = UInt16Argument, default=()):
        super().__init__(name, description)
        self.data_type = data_type
        self.length_type = length_type
        self.default = tuple(default)


class StringArgument(Argument):
    """ String. """

    def __init__(self, name: str, description: Optional[str] = None,
                 length_type: Argument = UInt16Argument, default=""):
        super().__init__(name, description)
        self.length_type = length_type
        self.default = str(default)


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

    Command(0x03, "light_state_center", arguments=[
        UInt16Argument("on_color_top"),     # TODO: Change to type.
        UInt16Argument("off_color_top"),
        UInt8Argument("on_frames_top"),
        UInt8Argument("off_frames_top"),
        UInt8Argument("transmission_on_frames_top"),
        UInt8Argument("transmission_off_frames_top"),
        Int16Argument("offset_top"),

        UInt16Argument("on_color_middle"),
        UInt16Argument("off_color_middle"),
        UInt8Argument("on_frames_middle"),
        UInt8Argument("off_frames_middle"),
        UInt8Argument("transmission_on_frames_middle"),
        UInt8Argument("transmission_off_frames_middle"),
        Int16Argument("offset_middle"),

        UInt16Argument("on_color_bottom"),
        UInt16Argument("off_color_bottom"),
        UInt8Argument("on_frames_bottom"),
        UInt8Argument("off_frames_bottom"),
        UInt8Argument("transmission_on_frames_bottom"),
        UInt8Argument("transmission_off_frames_bottom"),
        Int16Argument("offset_bottom"),

        UInt8Argument("unknown"),
    ]),
    Command(0x04, "cube_lights", arguments=[
        UInt16Argument("on_color_1"),
        UInt16Argument("off_color_1"),
        UInt8Argument("on_frames_1"),
        UInt8Argument("off_frames_1"),
        UInt8Argument("transmission_on_frames_1"),
        UInt8Argument("transmission_off_frames_1"),
        Int16Argument("offset_1"),

        UInt16Argument("on_color_2"),
        UInt16Argument("off_color_2"),
        UInt8Argument("on_frames_2"),
        UInt8Argument("off_frames_2"),
        UInt8Argument("transmission_on_frames_2"),
        UInt8Argument("transmission_off_frames_2"),
        Int16Argument("offset_2"),

        UInt16Argument("on_color_3"),
        UInt16Argument("off_color_3"),
        UInt8Argument("on_frames_3"),
        UInt8Argument("off_frames_3"),
        UInt8Argument("transmission_on_frames_3"),
        UInt8Argument("transmission_off_frames_3"),
        Int16Argument("offset_3"),

        UInt16Argument("on_color_4"),
        UInt16Argument("off_color_4"),
        UInt8Argument("on_frames_4"),
        UInt8Argument("off_frames_4"),
        UInt8Argument("transmission_on_frames_4"),
        UInt8Argument("transmission_off_frames_4"),
        Int16Argument("offset_4"),
    ]),

    Command(0x05, "object_connect", arguments=[
        UInt32Argument("factory_id"),
        BoolArgument("connect"),
    ]),

    Command(0x0b, "set_head_light", arguments=[
        BoolArgument("enable")
    ]),

    Command(0x10, "cube_id", arguments=[
        UInt32Argument("object_id"),
        UInt8Argument("rotation_period_frames"),
    ]),

    Command(0x11, "light_state_side", arguments=[
        UInt16Argument("on_color_left"),
        UInt16Argument("off_color_left"),
        UInt8Argument("on_frames_left"),
        UInt8Argument("off_frames_left"),
        UInt8Argument("transmission_on_frames_left"),
        UInt8Argument("transmission_off_frames_left"),
        Int16Argument("offset_left"),

        UInt16Argument("on_color_right"),
        UInt16Argument("off_color_right"),
        UInt8Argument("on_frames_right"),
        UInt8Argument("off_frames_right"),
        UInt8Argument("transmission_on_frames_right"),
        UInt8Argument("transmission_off_frames_right"),
        Int16Argument("offset_right"),

        UInt8Argument("unknown"),
    ]),

    Command(0x32, "drive_wheels", arguments=[
        FloatArgument("lwheel_speed_mmps"),
        FloatArgument("rwheel_speed_mmps"),
        FloatArgument("lwheel_accel_mmps2"),
        FloatArgument("rwheel_accel_mmps2"),
    ]),
    Command(0x33, "turn_in_place", arguments=[
        FloatArgument("wheel_speed_mmps"),
        FloatArgument("wheel_accel_mmps2"),
        Int16Argument("direction"),
    ]),
    Command(0x34, "drive_lift", arguments=[
        FloatArgument("speed"),
    ]),
    Command(0x35, "drive_head", arguments=[
        FloatArgument("speed"),
    ]),
    Command(0x36, "set_lift_height", arguments=[
        FloatArgument("height_mm"),
        FloatArgument("max_speed_rad_per_sec", default=3.0),
        FloatArgument("accel_rad_per_sec2", default=20.0),
        FloatArgument("duration_sec"),
        UInt8Argument("action_id"),
    ]),
    Command(0x37, "set_head_angle", arguments=[
        FloatArgument("angle_rad"),
        FloatArgument("max_speed_rad_per_sec", default=15.0),
        FloatArgument("accel_rad_per_sec2", default=20.0),
        FloatArgument("duration_sec"),
        UInt8Argument("action_id"),
    ]),
    Command(0x3b, "stop_all_motors"),

    Command(0x64, "set_robot_volume", arguments=[
        UInt16Argument("level"),
    ]),
    Command(0x8e, "output_audio", arguments=[
        FArrayArgument("samples", length=744),
    ]),

    Command(0x8f, "next_frame"),
    Command(0x97, "display_image", arguments=[
        VArrayArgument("image"),
    ]),

    Command(0xb4, "object_moved", arguments=[
        UInt32Argument("timestamp"),
        UInt32Argument("object_id"),
        FloatArgument("active_accel_x"),    # TODO: Change to type?
        FloatArgument("active_accel_y"),
        FloatArgument("active_accel_z"),
        UInt8Argument("axis_of_accel"),     # TODO: Change to enum?
    ]),
    Command(0xb5, "object_stopped_moving", arguments=[
        UInt32Argument("timestamp"),
        UInt32Argument("object_id"),
    ]),
    Command(0xb6, "object_tapped", arguments=[
        UInt32Argument("timestamp"),
        UInt32Argument("object_id"),
        UInt8Argument("num_taps"),
        UInt8Argument("tap_time"),
        UInt8Argument("tap_neg"),
        UInt8Argument("tap_pos"),
    ]),
    Command(0xb9, "object_tap_filtered", arguments=[
        UInt32Argument("timestamp"),
        UInt32Argument("object_id"),
        UInt8Argument("time"),
        UInt8Argument("intensity"),
    ]),

    Command(0xc4, "acknowledge_command", arguments=[
        UInt8Argument("action_id"),
    ]),

    Command(0xc2, "robot_delocalized"),
    Command(0xc3, "robot_poked"),

    Command(0xce, "object_power_state", arguments=[
        UInt32Argument("object_id"),
        UInt32Argument("missed_packets"),
        UInt8Argument("battery_level"),
    ]),
    Command(0xd0, "object_connection_state", arguments=[
        UInt32Argument("object_id"),
        UInt32Argument("factory_id"),
        UInt32Argument("object_type"),      # TODO: Change to enum.
        BoolArgument("connected"),
    ]),
    Command(0xd7, "object_up_axis_changed", arguments=[
        UInt32Argument("timestamp"),
        UInt32Argument("object_id"),
        UInt8Argument("axis"),              # TODO: Change to enum?
    ]),

    Command(0xdd, "falling_started", arguments=[
        UInt32Argument("unknown"),
    ]),
    Command(0xde, "falling_stopped", arguments=[
        UInt32Argument("unknown"),
        UInt32Argument("duration_ms"),
        FloatArgument("impact_intensity"),
    ]),

    Command(0xee, "firmware_signature", arguments=[
        UInt16Argument("unknown"),
        StringArgument("signature"),
    ]),
])
