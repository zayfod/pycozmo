"""

Protocol AST declaration.

"""

from .protocol_ast import *


FRAME_ID = b"COZ\x03RE\x01"
MIN_FRAME_SIZE = len(FRAME_ID) + 1 + 2 + 2 + 2

FIRST_ROBOT_PACKET_ID = 0xb0

FIRMWARE_VERSION = 2381


BODY_COLOR = Enum("BodyColor", members=[
    EnumMember("UNKNOWN", -1),
    EnumMember("WHITE_v10", 0),
    EnumMember("RESERVED", 1),
    EnumMember("WHITE_v15", 2),
    EnumMember("CE_LM_v15", 3),
    EnumMember("LE_BL_v16", 4),
])
NV_ENTRY_TAG = Enum("NvEntryTag", members=[
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
NV_OPERATION = Enum("NvOperation", members=[
    EnumMember("NVOP_READ", 0),
    EnumMember("NVOP_WRITE", 1),
    EnumMember("NVOP_ERASE", 2),
    EnumMember("NVOP_WIPEALL", 3),
])
NV_RESULT = Enum("NvResult", members=[
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
UP_AXIS = Enum("UpAxis", members=[
    EnumMember("XNegative", 0),
    EnumMember("XPositive", 1),
    EnumMember("YNegative", 2),
    EnumMember("YPositive", 3),
    EnumMember("ZNegative", 4),
    EnumMember("ZPositive", 5),
    EnumMember("NumAxes", 6),
    EnumMember("UnknownAxis", 7),
])
OBJECT_TYPE = Enum("ObjectType", members=[
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
IMAGE_ENCODING = Enum("ImageEncoding", members=[
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
IMAGE_RESOLUTION = Enum("ImageResolution", members=[
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
DEBUG_DATA_ID = Enum("DebugDataID", members=[
    EnumMember("MAC_ADDRESS", 0x1572),              # 624
])

LIGHT_STATE = Struct("LightState", arguments=[
    UInt16Argument("on_color"),
    UInt16Argument("off_color"),
    UInt8Argument("on_frames"),
    UInt8Argument("off_frames"),
    UInt8Argument("transition_on_frames"),
    UInt8Argument("transition_off_frames"),
    Int16Argument("offset"),
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
        DEBUG_DATA_ID,
    ],

    structs=[
        LIGHT_STATE,
    ],

    packets=[
        Connect(),
        Disconnect(),
        Ping(),
        Keyframe(),

        Command(0x03, "LightStateCenter", group="lights", arguments=[
            FArrayArgument("states", data_type=LIGHT_STATE, length=3),      # top, middle, bottom
            UInt8Argument("unknown"),
        ]),
        Command(0x04, "CubeLights", group="objects", arguments=[
            FArrayArgument("states", data_type=LIGHT_STATE, length=4)
        ]),
        Command(0x05, "ObjectConnect", group="objects", arguments=[
            UInt32Argument("factory_id"),
            BoolArgument("connect"),
        ]),
        Command(0x0b, "SetHeadLight", group="camera", arguments=[
            BoolArgument("enable")
        ]),
        Command(0x10, "CubeId", group="objects", arguments=[
            UInt32Argument("object_id"),
            UInt8Argument("rotation_period_frames"),
        ]),
        Command(0x11, "LightStateSide", group="lights", arguments=[
            FArrayArgument("states", data_type=LIGHT_STATE, length=2),      # left, right
            UInt8Argument("unknown"),
        ]),
        Command(0x25, "Enable", group="system"),
        Command(0x32, "DriveWheels", group="motors", arguments=[
            FloatArgument("lwheel_speed_mmps"),
            FloatArgument("rwheel_speed_mmps"),
            FloatArgument("lwheel_accel_mmps2"),
            FloatArgument("rwheel_accel_mmps2"),
        ]),
        Command(0x33, "TurnInPlaceAtSpeed", group="motors", arguments=[
            FloatArgument("wheel_speed_mmps"),
            FloatArgument("wheel_accel_mmps2"),
            Int16Argument("direction"),
        ]),
        Command(0x34, "MoveLift", group="motors", arguments=[
            FloatArgument("speed_rad_per_sec"),
        ]),
        Command(0x35, "MoveHead", group="motors", arguments=[
            FloatArgument("speed_rad_per_sec"),
        ]),
        Command(0x36, "SetLiftHeight", group="motors", arguments=[
            FloatArgument("height_mm"),
            FloatArgument("max_speed_rad_per_sec", default=3.0),
            FloatArgument("accel_rad_per_sec2", default=20.0),
            FloatArgument("duration_sec"),
            UInt8Argument("action_id"),
        ]),
        Command(0x37, "SetHeadAngle", group="motors", arguments=[
            FloatArgument("angle_rad"),
            FloatArgument("max_speed_rad_per_sec", default=15.0),
            FloatArgument("accel_rad_per_sec2", default=20.0),
            FloatArgument("duration_sec"),
            UInt8Argument("action_id"),
        ]),
        Command(0x39, "TurnInPlace", group="motors", arguments=[
            FloatArgument("angle_rad"),
            FloatArgument("speed_rad_per_sec"),
            FloatArgument("accel_rad_per_sec2"),
            FloatArgument("angle_tolerance_rad"),
            UInt8Argument("unknown4"),
            UInt8Argument("unknown5"),
            BoolArgument("is_absolute"),
            UInt8Argument("action_id"),
        ]),
        Command(0x3b, "StopAllMotors", group="motors"),
        Command(0x3d, "DriveStraight", group="motors", arguments=[
            FloatArgument("f0"),
            FloatArgument("f1"),
            FloatArgument("dist_mm"),               # minus ~20.3 mm?
            FloatArgument("f3"),
            FloatArgument("speed_mmps"),
            FloatArgument("f5"),
            FloatArgument("f6"),
        ]),
        Command(0x4b, "EnableBodyACC", group="system", arguments=[
            FArrayArgument("unknown", length=8, default=b"\xc4\xb6\x39\x00\x00\x00\xa0\xc1"),
        ]),
        Command(0x4c, "EnableCamera", group="camera", arguments=[
            BoolArgument("enable"),
            UInt8Argument("unknown", default=4)     # resolution but ignored?
        ]),
        Command(0x57, "SetCameraParams", group="camera", arguments=[
            FloatArgument("gain"),
            UInt16Argument("exposure_ms"),
            BoolArgument("auto_exposure_enabled"),
        ]),
        Command(0x60, "EnableStopOnCliff", group="motors", arguments=[
            BoolArgument("enable"),
        ]),
        Command(0x64, "SetRobotVolume", group="audio", arguments=[
            UInt16Argument("level"),
        ]),
        Command(0x66, "EnableColorImages", group="camera", arguments=[
            BoolArgument("enable"),
        ]),
        Command(0x81, "NvStorageOp", group="nv", arguments=[
            EnumArgument("tag", NV_ENTRY_TAG, data_type=UInt32Argument(), default=0xffffffff),
            Int32Argument("index"),
            EnumArgument("op", NV_OPERATION, data_type=UInt8Argument()),
            UInt8Argument("unknown"),
            VArrayArgument("data"),
        ]),
        Command(0x8e, "OutputAudio", group="audio", arguments=[
            FArrayArgument("samples", length=744),
        ]),
        Command(0x8f, "NextFrame", group="display"),
        Command(0x93, "AnimHead", group="anim", arguments=[
            UInt8Argument("duration_ms"),
            Int8Argument("variability_deg"),
            Int8Argument("angle_deg"),
        ]),
        Command(0x94, "AnimLift", group="anim", arguments=[
            UInt8Argument("duration_ms"),
            UInt8Argument("variability_mm"),
            UInt8Argument("height_mm"),
        ]),
        Command(0x97, "DisplayImage", group="display", arguments=[
            VArrayArgument("image"),
        ]),
        Command(0x98, "AnimBackpackLights", group="anim", arguments=[
            FArrayArgument("colors", data_type=UInt16Argument(), length=5),  # left, front, middle, back, right
        ]),
        Command(0x99, "AnimBody", group="anim", arguments=[
            Int16Argument("speed"),
            Int16Argument("unknown1"),
        ]),
        Command(0x9a, "EndAnimation", group="anim"),
        Command(0x9b, "StartAnimation", group="anim", arguments=[
            UInt8Argument("anim_id")
        ]),
        Command(0x9f, "EnableAnimationState", group="system"),
        Command(0xaf, "FirmwareUpdate", group="firmware", arguments=[
            UInt16Argument("chunk_id"),
            FArrayArgument("data", length=1024)
        ]),

        Command(0xb0, "DebugData", group="debug", arguments=[
            UInt16Argument("debug_id"),             # See DebugDataID
            UInt16Argument("unused"),               # Always 0
            UInt16Argument("unknown2"),             # Source? Observed: 1, 100, 110, 1203, 1204, 1213, 169, 171, 172, 228, 247, 249, 252, 282, 330, 341, 368, 372, 374, 391, 394, 398, 40, 405, 409, 411, 413, 414, 417, 52, 57
            Int8Argument("unknown3"),               # Level? Observed: -1, 1, 2, 3, 5
            VArrayArgument("data", data_type=UInt32Argument(), length_type=UInt8Argument())
        ]),
        Command(0xb4, "ObjectMoved", group="objects", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("object_id"),
            FloatArgument("active_accel_x"),
            FloatArgument("active_accel_y"),
            FloatArgument("active_accel_z"),
            EnumArgument("axis_of_accel", UP_AXIS, data_type=UInt8Argument(), default=7),
        ]),
        Command(0xb5, "ObjectStoppedMoving", group="objects", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("object_id"),
        ]),
        Command(0xb6, "ObjectTapped", group="objects", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("object_id"),
            UInt8Argument("num_taps"),
            UInt8Argument("tap_time"),
            Int8Argument("tap_neg"),
            Int8Argument("tap_pos"),
        ]),
        Command(0xb9, "ObjectTapFiltered", group="objects", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("object_id"),
            UInt8Argument("time"),
            UInt8Argument("intensity"),
        ]),
        Command(0xc4, "AcknowledgeAction", group="motors", arguments=[
            UInt8Argument("action_id"),
        ]),
        Command(0xc2, "RobotDelocalized", group="localization"),
        Command(0xc3, "RobotPoked", group="localization"),
        Command(0xc9, "HardwareInfo", group="system", arguments=[
            UInt32Argument("serial_number_head"),
            UInt8Argument("unknown1"),
            UInt8Argument("unknown2"),
        ]),
        Command(0xca, "AnimationStarted", group="anim", arguments=[
            UInt8Argument("anim_id")
        ]),
        Command(0xcb, "AnimationEnded", group="anim", arguments=[
            UInt8Argument("anim_id")
        ]),
        Command(0xcd, "NvStorageOpResult", group="nv", arguments=[
            EnumArgument("tag", NV_ENTRY_TAG, data_type=UInt32Argument(), default=0xffffffff),
            Int32Argument("index"),
            EnumArgument("op", NV_OPERATION, data_type=UInt8Argument()),
            EnumArgument("result", NV_RESULT, data_type=Int8Argument()),
            VArrayArgument("data"),
        ]),
        Command(0xce, "ObjectPowerLevel", group="objects", arguments=[
            UInt32Argument("object_id"),
            UInt32Argument("missed_packets"),
            UInt8Argument("battery_level"),
        ]),
        Command(0xd0, "ObjectConnectionState", group="objects", arguments=[
            UInt32Argument("object_id"),
            UInt32Argument("factory_id"),
            EnumArgument("object_type", OBJECT_TYPE, data_type=Int32Argument(), default=-1),
            BoolArgument("connected"),
        ]),
        Command(0xd7, "ObjectUpAxisChanged", group="objects", arguments=[
            UInt32Argument("timestamp"),
            UInt32Argument("object_id"),
            EnumArgument("axis", UP_AXIS, data_type=UInt8Argument(), default=7),
        ]),
        Command(0xdb, "ButtonPressed", group="system", arguments=[
            BoolArgument("pressed"),
        ]),
        Command(0xdd, "FallingStarted", group="localization", arguments=[
            UInt32Argument("unknown"),
        ]),
        Command(0xde, "FallingStopped", group="localization", arguments=[
            UInt32Argument("unknown"),
            UInt32Argument("duration_ms"),
            FloatArgument("impact_intensity"),
        ]),
        Command(0xed, "BodyInfo", group="system", arguments=[
            UInt32Argument("serial_number"),
            UInt32Argument("body_hw_version"),
            EnumArgument("body_color", BODY_COLOR, data_type=Int32Argument(), default=-1),
        ]),
        Command(0xee, "FirmwareSignature", group="system", arguments=[
            UInt16Argument("unknown"),          # Last 2 bytes of head s/n?
            StringArgument("signature"),
        ]),
        Command(0xef, "FirmwareUpdateResult", group="firmware", arguments=[
            UInt32Argument("byte_count"),
            UInt16Argument("chunk_id"),
            UInt8Argument("status"),            # 0=OK; 0x0a=complete?
        ]),

        Event(0xf0, "RobotState", group="state", arguments=[
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
            FArrayArgument("cliff_data_raw", data_type=UInt16Argument(), length=4),
            UInt16Argument("backpack_touch_sensor_raw"),
            UInt8Argument("curr_path_segment"),
        ]),
        Event(0xf1, "AnimationState", group="state", arguments=[
            UInt32Argument("timestamp"),
            Int32Argument("num_anim_bytes_played"),
            Int32Argument("num_audio_frames_played"),
            UInt8Argument("enabled_anim_tracks"),
            UInt8Argument("tag"),
            UInt8Argument("client_drop_count"),
        ]),
        Event(0xf2, "ImageChunk", group="state", arguments=[
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
        Event(0xf3, "ObjectAvailable", group="state", arguments=[
            UInt32Argument("factory_id"),
            EnumArgument("object_type", OBJECT_TYPE, data_type=Int32Argument(), default=-1),
            Int8Argument("rssi"),
        ]),
        Event(0xf4, "ImageImuData", group="state", arguments=[
            UInt32Argument("image_id"),
            FloatArgument("rate_x"),
            FloatArgument("rate_y"),
            FloatArgument("rate_z"),
            UInt8Argument("line_2_number"),
        ]),
    ]

)
