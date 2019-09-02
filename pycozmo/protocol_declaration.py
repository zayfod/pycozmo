"""

Protocol AST declaration.

"""

from .protocol_ast import *


FRAME_ID = b"COZ\x03RE\x01"
MIN_FRAME_SIZE = len(FRAME_ID) + 1 + 2 + 2 + 2


PROTOCOL = Protocol(

    structs=[
        Struct("light_state", arguments=[
            UInt16Argument("on_color"),
            UInt16Argument("off_color"),
            UInt8Argument("on_frames"),
            UInt8Argument("off_frames"),
            UInt8Argument("transmission_on_frames"),
            UInt8Argument("transmission_off_frames"),
            Int16Argument("offset"),
        ]),
    ],

    packets=[
        Connect(),
        Disconnect(),
        Ping(),
        Unknown0A(),

        Command(0x03, "light_state_center", arguments=[
            FArrayArgument("states", data_type="LightState", length=3),     # top, middle, bottom
            UInt8Argument("unknown"),
        ]),
        Command(0x04, "cube_lights", arguments=[
            FArrayArgument("states", data_type="LightState", length=4)
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
            FArrayArgument("states", data_type="LightState", length=2),     # left, right
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

        Command(0x4c, "enable_camera", arguments=[
            BoolArgument("enable"),
            UInt8Argument("unknown", default=4)
        ]),

        Command(0x57, "set_camera_params", arguments=[
            FloatArgument("gain"),
            UInt16Argument("exposure_ms"),
            BoolArgument("auto_exposure_enabled"),
        ]),

        Command(0x60, "enable_stop_on_cliff", arguments=[
            BoolArgument("enable"),
        ]),

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

        Command(0xc9, "hardware_info", arguments=[
            UInt32Argument("serial_number_head"),
            UInt8Argument("unknown1"),          # body_hw_version?
            UInt8Argument("unknown2"),          # body_color?
        ]),

        Command(0xce, "object_power_level", arguments=[
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

        Event(0xf0, "robot_state", arguments=[
            UInt32Argument("timestamp"),
            FloatArgument("unknown1"),
            FloatArgument("unknown2"),
            FloatArgument("x"),
            FloatArgument("y"),
            FloatArgument("z"),
            FloatArgument("pose_angle_rad"),
            FloatArgument("pose_pitch_rad"),
            FloatArgument("lwheel_speed_mmps"),
            FloatArgument("rwheel_speed_mmps"),
            FloatArgument("head_angle_rad"),
            FloatArgument("lift_height_mm"),
            FloatArgument("accel_x"),
            FloatArgument("accel_y"),
            FloatArgument("accel_z"),
            FloatArgument("gyro_x"),
            FloatArgument("gyro_y"),
            FloatArgument("gyro_z"),
            FloatArgument("battery_voltage"),
            FloatArgument("unknown19"),
            FloatArgument("unknown20"),
            FloatArgument("unknown21"),
            UInt8Argument("unknown22"),
            UInt8Argument("unknown23"),
            UInt8Argument("unknown24"),
        ]),

        Event(0xf2, "image_chunk", arguments=[
            UInt32Argument("frame_timestamp"),
            UInt32Argument("image_id"),
            UInt32Argument("chunk_debug"),
            UInt8Argument("image_encoding"),
            UInt8Argument("image_resolution"),  # TODO: Should be an enumeration.
            UInt8Argument("image_chunk_count"),
            UInt8Argument("chunk_id"),
            UInt16Argument("status"),
            VArrayArgument("data"),
        ]),
    ]

)
