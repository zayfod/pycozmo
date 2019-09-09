"""

Protocol AST declaration.

"""

from .protocol_ast import *


FRAME_ID = b"COZ\x03RE\x01"
MIN_FRAME_SIZE = len(FRAME_ID) + 1 + 2 + 2 + 2

FIRMWARE_VERSION = 2381


BODY_COLOR = Enum("body_color", members=[
    EnumMember("UNKNOWN", -1),
    EnumMember("WHITE_v10", 0),
    EnumMember("RESERVED", 1),
    EnumMember("WHITE_v15", 2),
    EnumMember("CE_LM_v15", 3),
    EnumMember("LE_BL_v16", 4),
])
NV_ENTRY_TAG = Enum("nv_entry_tag", members=[
    EnumMember("NVEntry_Invalid", 0xffffffff),
    EnumMember("NVEntry_GameSkillLevels", 0x180000),
    EnumMember("NVEntry_OnboardingData", 0x181000),
    EnumMember("NVEntry_GameUnlocks", 0x182000),
    EnumMember("NVEntry_FaceEnrollData", 0x183000),
    EnumMember("NVEntry_FaceAlbumData", 0x184000),
    EnumMember("NVEntry_NurtureGameData", 0x194000),
    EnumMember("NVEntry_InventoryData", 0x195000),
    EnumMember("NVEntry_LabAssignments", 0x196000),
    EnumMember("NVEntry_SavedCubeIDs", 0x197000),
    EnumMember("NVEntry_NEXT_SLOT", 0x198000),
    EnumMember("NVEntry_FACTORY_RESERVED1", 0x1c0000),
    EnumMember("NVEntry_FACTORY_RESERVED2", 0x1de000),
    EnumMember("NVEntry_BirthCertificate", 0x80000000),
    EnumMember("NVEntry_CameraCalib", 0x80000001),
    EnumMember("NVEntry_ToolCodeInfo", 0x80000002),
    EnumMember("NVEntry_CalibPose", 0x80000003),
    EnumMember("NVEntry_CalibMetaInfo", 0x80000004),
    EnumMember("NVEntry_ObservedCubePose", 0x80000005),
    EnumMember("NVEntry_IMUInfo", 0x80000006),
    EnumMember("NVEntry_CliffValOnDrop", 0x80000007),
    EnumMember("NVEntry_CliffValOnGround", 0x80000008),
    EnumMember("NVEntry_PlaypenTestResults", 0x80000010),
    EnumMember("NVEntry_FactoryLock", 0x80000011),
    EnumMember("NVEntry_VersionMagic", 0x80000012),
    EnumMember("NVEntry_CalibImage1", 0x80010000),
    EnumMember("NVEntry_CalibImage2", 0x80020000),
    EnumMember("NVEntry_CalibImage3", 0x80030000),
    EnumMember("NVEntry_CalibImage4", 0x80040000),
    EnumMember("NVEntry_CalibImage5", 0x80050000),
    EnumMember("NVEntry_CalibImage6", 0x80060000),
    EnumMember("NVEntry_ToolCodeImageLeft", 0x80100000),
    EnumMember("NVEntry_ToolCodeImageRight", 0x80110000),
    EnumMember("NVEntry_PrePlaypenResults", 0xc0000000),
    EnumMember("NVEntry_PrePlaypenCentroids", 0xc0000001),
    EnumMember("NVEntry_IMUAverages", 0xc0000004),
    EnumMember("NVEntry_FactoryBaseTag", 0xde000),
    EnumMember("NVEntry_FactoryBaseTagWithBCOffset", 0xde030),
])
NV_OPERATION = Enum("nv_operation", members=[
    EnumMember("NVOP_READ", 0),
    EnumMember("NVOP_WRITE", 1),
    EnumMember("NVOP_ERASE", 2),
    EnumMember("NVOP_WIPEALL", 3),
])
NV_RESULT = Enum("nv_result", members=[
    EnumMember("NV_OKAY", 0),
    EnumMember("NV_SCHEDULED", 1),
    EnumMember("NV_NO_DO", 2),
    EnumMember("NV_MORE", 3),
    EnumMember("NV_UNKNOWN_4", 4),
    EnumMember("NV_UNKNOWN_5", 5),
    EnumMember("NV_UNKNOWN_6", 6),
    EnumMember("NV_UNKNOWN_7", 7),
    EnumMember("NV_UNKNOWN_8", 8),
    EnumMember("NV_NOT_FOUND", -1),
    EnumMember("NV_NO_ROOM", -2),
    EnumMember("NV_ERROR", -3),
    EnumMember("NV_TIMEOUT", -4),
    EnumMember("NV_BUSY", -5),
    EnumMember("NV_BAD_ARGS", -6),
    EnumMember("NV_NO_MEM", -7),
    EnumMember("NV_LOOP", -8),
    EnumMember("NV_CORRUPT", -9),
])
UP_AXIS = Enum("up_axis", members=[
    EnumMember("XNegative", 0),
    EnumMember("XPositive", 1),
    EnumMember("YNegative", 2),
    EnumMember("YPositive", 3),
    EnumMember("ZNegative", 4),
    EnumMember("ZPositive", 5),
    EnumMember("NumAxes", 6),
    EnumMember("UnknownAxis", 7),
])
OBJECT_TYPE = Enum("object_type", members=[
    EnumMember("InvalidObject", -1),
    EnumMember("UnknownObject", 0),
    EnumMember("Block_LIGHTCUBE1", 1),
    EnumMember("Block_LIGHTCUBE2", 2),
    EnumMember("Block_LIGHTCUBE3", 3),
    EnumMember("Block_LIGHTCUBE_GHOST", 4),
    EnumMember("FlatMat_GEARS_4x4", 5),
    EnumMember("FlatMat_LETTERS_4x4", 6),
    EnumMember("FlatMat_ANKI_LOGO_8BIT", 7),
    EnumMember("FlatMat_LAVA_PLAYTEST", 8),
    EnumMember("Platform_LARGE", 9),
    EnumMember("Bridge_LONG", 10),
    EnumMember("Bridge_SHORT", 11),
    EnumMember("Ramp_Basic", 12),
    EnumMember("Charger_Basic", 13),
    EnumMember("ProxObstacle", 14),
    EnumMember("CliffDetection", 15),
    EnumMember("CollisionObstacle", 16),
    EnumMember("CustomType00", 17),
    EnumMember("CustomType01", 18),
    EnumMember("CustomType02", 19),
    EnumMember("CustomType03", 20),
    EnumMember("CustomType04", 21),
    EnumMember("CustomType05", 22),
    EnumMember("CustomType06", 23),
    EnumMember("CustomType07", 24),
    EnumMember("CustomType08", 25),
    EnumMember("CustomType09", 26),
    EnumMember("CustomType10", 27),
    EnumMember("CustomType11", 28),
    EnumMember("CustomType12", 29),
    EnumMember("CustomType13", 30),
    EnumMember("CustomType14", 31),
    EnumMember("CustomType15", 32),
    EnumMember("CustomType16", 33),
    EnumMember("CustomType17", 34),
    EnumMember("CustomType18", 35),
    EnumMember("CustomType19", 36),
    EnumMember("CustomFixedObstacle", 37),
])
IMAGE_ENCODING = Enum("image_encoding", members=[
    EnumMember("NoneImageEncoding", 0),
    EnumMember("RawGray", 1),
    EnumMember("RawRGB", 2),
    EnumMember("YUYV", 3),
    EnumMember("BAYER", 4),
    EnumMember("JPEGGray", 5),
    EnumMember("JPEGColor", 6),
    EnumMember("JPEGColorHalfWidth", 7),
    EnumMember("JPEGMinimizedGray", 8),
    EnumMember("JPEGMinimizedColor", 9),
])
IMAGE_RESOLUTION = Enum("image_resolution", members=[
    EnumMember("VerificationSnapshot", 0),
    EnumMember("QQQQVGA", 1),
    EnumMember("QQQVGA", 2),
    EnumMember("QQVGA", 3),
    EnumMember("QVGA", 4),
    EnumMember("CVGA", 5),
    EnumMember("VGA", 6),
    EnumMember("SVGA", 7),
    EnumMember("XGA", 8),
    EnumMember("SXGA", 9),
    EnumMember("UXGA", 10),
    EnumMember("QXGA", 11),
    EnumMember("QUXGA", 12),
    EnumMember("ImageResolutionCount", 13),
    EnumMember("ImageResolutionNone", 14),
])


PROTOCOL = Protocol(

    enums=[
        BODY_COLOR,
        NV_ENTRY_TAG,
        NV_OPERATION,
        NV_RESULT,
        UP_AXIS,
        OBJECT_TYPE,
        IMAGE_ENCODING,
        IMAGE_RESOLUTION,
    ],

    structs=[
        Struct("light_state", arguments=[
            UInt16Argument("on_color"),
            UInt16Argument("off_color"),
            UInt8Argument("on_frames"),
            UInt8Argument("off_frames"),
            UInt8Argument("transition_on_frames"),
            UInt8Argument("transition_off_frames"),
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
        Command(0x25, "enable"),
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
            EnumArgument("tag", NV_ENTRY_TAG, data_type=UInt32Argument, default=0xffffffff),
            Int32Argument("index"),
            EnumArgument("op", NV_OPERATION, data_type=UInt8Argument),
            UInt8Argument("unknown"),
            VArrayArgument("data"),
        ]),
        Command(0x8e, "output_audio", arguments=[
            FArrayArgument("samples", length=744),
        ]),
        Command(0x8f, "next_frame"),
        Command(0x97, "display_image", arguments=[
            VArrayArgument("image"),
        ]),
        Command(0xaf, "firmware_update", arguments=[
            UInt16Argument("chunk_id"),
            FArrayArgument("data", length=1024)
        ]),
        Command(0xb0, "unknown_b0", arguments=[
            UInt16Argument("unknown0"),
            UInt16Argument("unknown1"),
            UInt16Argument("unknown2"),
            Int8Argument("unknown3"),
            VArrayArgument("unknown4", data_type=UInt32Argument, length_type=UInt8Argument)
        ]),
        Command(0xb4, "object_moved", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("object_id"),
            FloatArgument("active_accel_x"),
            FloatArgument("active_accel_y"),
            FloatArgument("active_accel_z"),
            EnumArgument("axis_of_accel", UP_AXIS, data_type=UInt8Argument, default=7),
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
            Int8Argument("tap_neg"),
            Int8Argument("tap_pos"),
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
            EnumArgument("tag", NV_ENTRY_TAG, data_type=UInt32Argument, default=0xffffffff),
            Int32Argument("index"),
            EnumArgument("op", NV_OPERATION, data_type=UInt8Argument),
            EnumArgument("result", NV_RESULT, data_type=Int8Argument),
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
            EnumArgument("object_type", OBJECT_TYPE, data_type=Int32Argument, default=-1),
            BoolArgument("connected"),
        ]),
        Command(0xd7, "object_up_axis_changed", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("object_id"),
            EnumArgument("axis", UP_AXIS, data_type=UInt8Argument, default=7),
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
            EnumArgument("body_color", BODY_COLOR, data_type=Int32Argument, default=-1),
        ]),
        Command(0xee, "firmware_signature", arguments=[
            UInt16Argument("unknown"),          # Last 2 bytes of head s/n?
            StringArgument("signature"),
        ]),
        Command(0xef, "firmware_update_result", arguments=[
            UInt32Argument("byte_count"),
            UInt16Argument("chunk_id"),
            UInt8Argument("status"),            # 0=OK; 0x0a=complete?
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
            Int32Argument("num_anim_bytes_played"),
            Int32Argument("num_audio_frames_played"),
            UInt8Argument("enabled_anim_tracks"),
            UInt8Argument("tag"),
            UInt8Argument("client_drop_count"),
        ]),
        Event(0xf2, "image_chunk", arguments=[
            UInt32Argument("frame_timestamp"),
            UInt32Argument("image_id"),
            UInt32Argument("chunk_debug"),
            EnumArgument("image_encoding", IMAGE_ENCODING),
            EnumArgument("image_resolution", IMAGE_RESOLUTION),
            UInt8Argument("image_chunk_count"),
            UInt8Argument("chunk_id"),
            UInt16Argument("status"),
            VArrayArgument("data"),
        ]),
        Event(0xf3, "object_available", arguments=[
            UInt32Argument("factory_id"),
            EnumArgument("object_type", OBJECT_TYPE, data_type=Int32Argument, default=-1),
            Int8Argument("rssi"),
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
