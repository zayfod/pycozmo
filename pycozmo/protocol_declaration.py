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
            UInt8Argument("unknown", default=4)     # resolution but ignored?
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
        Command(0x66, "enable_color_images", arguments=[
            BoolArgument("enable"),
        ]),
        Command(0x81, "nv_storage_op", arguments=[
            UInt32Argument("tag"),
            UInt32Argument("unknown"),
            UInt8Argument("op"),
            UInt8Argument("index"),
            VArrayArgument("data"),
        ]),
        Command(0x8e, "output_audio", arguments=[
            FArrayArgument("samples", length=744),
        ]),
        Command(0x8f, "next_frame"),
        Command(0x97, "display_image", arguments=[
            VArrayArgument("image"),
        ]),
        Command(0xb0, "unknown_b0", arguments=[
            UInt16Argument("unknown0"),
            UInt16Argument("unknown1"),
            UInt16Argument("unknown2"),
            UInt8Argument("unknown3"),
            VArrayArgument("unknown4", data_type=UInt32Argument, length_type=UInt8Argument)
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
            UInt8Argument("unknown1"),
            UInt8Argument("unknown2"),
        ]),
        Command(0xcd, "nv_storage_op_result", arguments=[
            UInt32Argument("tag"),
            UInt32Argument("result"),
            UInt8Argument("op"),
            UInt8Argument("index"),
            VArrayArgument("data"),
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
        Command(0xed, "body_info", arguments=[
            UInt32Argument("serial_number"),
            UInt32Argument("body_hw_version"),
            UInt32Argument("body_color"),
        ]),
        Command(0xee, "firmware_signature", arguments=[
            UInt16Argument("unknown"),          # Last 2 bytes of head s/n?
            StringArgument("signature"),
        ]),

        Event(0xf0, "robot_state", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("pose_frame_id"),
            UInt32Argument("pose_origin_id"),
            FloatArgument("pose_x"),
            FloatArgument("pose_y"),
            FloatArgument("pose_z"),
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
            UInt32Argument("status"),
            FArrayArgument("cliff_data_raw", data_type=UInt16Argument, length=4),
            UInt16Argument("backpack_touch_sensor_raw"),
            UInt8Argument("curr_path_segment"),
        ]),
        Event(0xf1, "animation_state", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("num_anim_bytes_played"),
            UInt32Argument("num_audio_frames_played"),
            UInt8Argument("enabled_anim_tracks"),
            UInt8Argument("tag"),
            UInt8Argument("client_drop_count"),
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
        Event(0xf3, "object_available", arguments=[
            UInt32Argument("factory_id"),
            UInt32Argument("object_type"),
            UInt8Argument("rssi"),
        ]),
        Event(0xf4, "image_imu_data", arguments=[
            UInt32Argument("image_id"),
            FloatArgument("rate_x"),
            FloatArgument("rate_y"),
            FloatArgument("rate_z"),
            UInt8Argument("line_2_number"),
        ]),
    ]

)
