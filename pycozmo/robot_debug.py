"""

Cozmo firmware debug message decoding.

Based on AnkiLogStringTables.json .

"""

from typing import List, Any, Optional
import logging


# Map of robot log levels to Python log levels.
ROBOT_LOG_LEVELS = {
    1: logging.DEBUG,
    2: logging.DEBUG,
    3: logging.INFO,
    4: logging.WARNING,
    5: logging.ERROR,
    6: logging.CRITICAL,
}

# Map of robot debug name IDs to strings.
ROBOT_NAME_IDS = {
    0: "ASSERT",
    1: "wifi.dropped_traces",
    2: "rtip.dropped_traces",
    3: "body.dropped_traces",
    395: "AnimationController.Init",
    388: "AnimationController.engine_init.refused",
    377: "AnimationController.Clear",
    136: "AnimationController.BufferCorrupt",
    378: "AnimationController.buffer_key_frame.not_animCtrlState",
    379: "AnimationController.BufferKeyFrame.BufferFull",
    380: "AnimationController.BufferKeyFrame",
    169: "AnimationController.IsReadyToPlay.BufferStarved",
    404: "AnimationController.advance_audio.currupt_buffer",
    177: "AnimationController.ExpectedAudio",
    178: "AnimationController.BufferUnexpectedlyEmpty",
    168: "AnimationController.StartOfAnimation",
    166: "AnimationController.EndOfAnimation",
    381: "AnimationController.RequestHeadAngle",
    382: "AnimationController.RequestLiftHeight",
    383: "AnimationController.SetBackpackLEDs",
    384: "AnimationController.SetFaceFrame",
    385: "AnimationController.event",
    386: "AnimationController.SetBodyMotion",
    1209: "AnimationController.RecordHeading",
    1210: "AnimationController.SetTurnToRecordedHeading",
    167: "AnimationController.UnexpectedTag",
    387: "AnimationController.termination",
    219: "CozmoBot.InitFail.HAL",
    227: "CozmoBot.InitFail.AnimationController",
    220: "CozmoBot.InitFail.Messages",
    221: "CozmoBot.InitFail.Localization",
    222: "CozmoBot.InitFail.PathFollower",
    366: "CozmoBot.InitFail.IMUFilter",
    224: "CozmoBot.InitFail.DockingController",
    225: "CozmoBot.InitFail.PickAndPlaceController",
    226: "CozmoBot.InitFail.LiftController",
    94: "CozmoBot.TicsPerSec",
    228: "CozmoBot.Radio.Connected",
    229: "CozmoBot.Radio.Disconnected",
    230: "CozmoBot.Main.AnimationControllerUpdateFailed",
    179: "CozmoBot.BroadcastingAvailability",
    231: "CozmoBot.InvalidMode",
    1236: "CozmoBot.step_LongExecution.CompressAndSendFailed",
    5: "DockingController",
    1201: "DockingController.GetVerticalFOV.ZeroFOV",
    1202: "DockingController.GetHorizontalFOV.ZeroFOV",
    362: "DockingController.Init.NullHeadCamInfo",
    1199: "DockingController.SetCameraFieldOfView.Values",
    299: "DockingController.Update.BackingUpAndStopping",
    300: "DockingController.Update.TrackerPeriod",
    301: "DockingController.Update.NoLongerPastPointOfNoReturn",
    302: "DockingController.Update.ReceivedErrorSignal",
    303: "DockingController.Update.MarkerExpectedInsideFOV",
    304: "DockingController.Update.MarkerExpectedOutsideFOV",
    305: "DockingController.Update.PointOfNoReturn",
    306: "DockingController.LOOKING_FOR_BLOCK.TooLongWithoutErrorSignal",
    307: "DockingController.APPROACH_FOR_DOCK.TooLongWithoutErrorSignal",
    308: "DockingController.Update.FinishedPathButErrorSignalTooLarge_1",
    309: "DockingController.Update.AbleToDoHannsManeuver_1",
    310: "DockingController.Update.FinishedPathButErrorSignalTooLarge_2",
    311: "DockingController.Update.AbleToDoHannsManeuver_2",
    312: "DockingController.Update.ExecutingHannsManeuver",
    313: "DockingController.Update.BackingUp",
    314: "DockingController.Update.TooManyDockingFails",
    1212: "DockingController.Update.Success",
    316: "DockingController.Update.DockingSucces",
    317: "DockingController.Update.InvalidMode",
    318: "DockingController.SetRelDockPose.OORErrorSignal",
    320: "DockingController.SetRelDockPose.DockPoseReached",
    321: "DockingController.SetRelDockPose",
    322: "DockingController.SetRelDockPose.AcquireNewSignal",
    323: "DockingController.SetRelDockPose.MarkerInsideFOV",
    324: "DockingController.SetRelDockPose.DubinsPathFailed",
    325: "DockingController.SetRelDockPose.FailedToCreatePath",
    282: "HeadController.CalibratedWhileApplyingPower",
    283: "HeadController.Calibrated",
    7: "HeadController",
    399: "HeadController.SetDesiredAngle.VPGFixedDurationFailed",
    54: "HeadController.MotorBurnoutProtection",
    284: "HeadController.SetGains",
    187: "IMUFilter.EnableBraceWhenFalling",
    329: "IMUFilter.PokeDetected.Gyro",
    330: "IMUFilter.PokeDetected.Accel",
    368: "IMUFilter.PDWhileStationary",
    421: "IMUFilter.PickupDetected",
    25: "IMUFilter",
    182: "RobotPitch",
    392: "IMUFilter.Update.GyroBiasInit",
    391: "IMUFilter.Bias",
    393: "IMUFilter.Update.GyroCalibrated",
    335: "IMUFilter.IMURecording.Complete",
    336: "IMUFilter.IMURecording.CompleteRaw",
    337: "IMUFilter.IMURecording.Start",
    16: "LiftController",
    400: "LiftController.SetDesiredHeight.VPGFixedDurationFailed",
    418: "LiftController.Update.NoLoadDetected",
    419: "LiftController.Update.LoadDetected",
    420: "LiftController.Update.CheckingForLoad",
    389: "LiftController.Update.Values",
    390: "LiftController.Update.Power",
    280: "LiftController.SetGains",
    55: "Localization.InterpolatePose.PosesOutOfOrder",
    56: "Localization.InterpolatePose.TargetTimeOOR",
    57: "Localization.UpdatePoseWithKeyFrame.SettingPose",
    58: "Localization.UpdatePoseWithKeyFrame.TimeNotFound",
    59: "Localization.UpdatePoseWithKeyFrame.IgnoreOldKeyframe",
    60: "Localization.GetHistPoseAtTime.NoHistory",
    61: "Localization.GetHistPoseAtTime.TimeTooOld",
    62: "Localization.GetHistPoseAtTime.TimeTooNew",
    106: "Messages.ProcessBadTag_EngineToRobot.Recvd",
    107: "Messages.StillLookingForID.Timeout",
    100: "Messages.Process_syncTime.Recvd",
    414: "watchdog_reset_count",
    115: "Messages.Process_absLocalizationUpdate.Recvd",
    394: "Messages.Update.GyroCalibrated",
    1205: "ReliableTransport.PacketNotAccepted",
    103: "Messages.Process_executePath.StartingPath",
    422: "Messages.Process_dockWithObject.Recvd",
    108: "Messages.Process_placeObjectOnGround.Recvd",
    338: "Messages.Process_drive.IgnoringBecauseAlreadyOnPath",
    116: "Messages.Process_drive.Executing",
    109: "Messages.Process_liftHeight.Recvd",
    117: "Messages.Process_headAngle.Recvd",
    118: "Messages.Process_turnInPlaceAtSpeed.Recvd",
    110: "Messages.Process_imageRequest.Recvd",
    1200: "Messages.Process_cameraFOVInfo.Unsupported",
    114: "Messages.Process_setControllerGains.InvalidController",
    1195: "Messages.enableMotorPower.UnhandledMotorID",
    162: "ReadToolCodeMode",
    119: "Receiver.ReceiveData.Invalid",
    120: "Receiver.ReceiveData.SizeError",
    121: "Receiver_OnConnectionRequest",
    122: "Receiver_OnConnected",
    123: "Receiver_OnDisconnect",
    163: "nvstorage.simulator_get_camera_calib.calib_not_found",
    375: "nvstorage.invalid_operation",
    253: "Path.GetLength.UndefinedSegment",
    254: "Path.OffsetStart.UndefinedSegment",
    255: "Path.GetStartPoint.UndefinedSegment",
    256: "Path.GetEndPose.UndefinedSegment",
    257: "Path.Print.Line",
    258: "Path.Print.Arc",
    259: "Path.Print.Turn",
    260: "Path.GetDistToSegment.UndefinedSegment",
    261: "Path.GetDistToLineSegment",
    6: "Path",
    262: "Path.GetDistToArcSegment",
    263: "Path.GetDistToPointTurnSegment",
    264: "Path.PrintSegment",
    265: "Path.GenerateDubinsPath.InvalidSegment",
    266: "Path.CheckSegmentContinuity.Fail_NoExist",
    267: "Path.CheckSegmentContinuity.Fail",
    268: "Path.AppendLine.ExceededMaxSize",
    269: "Path.AppendLine",
    270: "Path.AddArc.ZeroSweep",
    271: "Path.AddArc",
    272: "Path.AppendArc.ExceededMaxSize",
    273: "Path.AppendArc.ZeroSweep",
    274: "Path.AppendPointTurn.ExceededMaxSize",
    275: "Path.AppendSegment.ExceededMaxSize",
    276: "Path.AppendSegment",
    342: "PathFollower.GetClosestSegment.PathDist",
    343: "PathFollower.GetClosestSegment",
    344: "PathFollower.StartPathTraversal.PathIsDiscontinuous",
    345: "PathFollower.StartPathTraversal",
    33: "PathFollower",
    346: "PathFollower.ProcessPathSegment.Decel",
    347: "PathFollower.ProcessPathSegmentPointTurn",
    348: "PathFollower.ProcessPathSegmentPointTurn.ExecutePointTurn",
    349: "PathFollower.PathComplete",
    350: "PathFollower.Update.InvalidSegmentType",
    351: "PathFollower.Update.DistToPath",
    352: "PathFollower.Update.SegmentSpeed",
    353: "PathFollower.Update.StartingErrorTooLarge",
    95: "PathFollower.DriveStraight.NegativeFraction",
    354: "PathFollower.DriveStraight.VPGFail",
    355: "PathFollower.DriveStraight.Params",
    356: "PathFollower.DriveStraight.Accels",
    357: "PathFollower.DriveStraight.Points",
    99: "PathFollower.DriveArc.NegativeFraction",
    358: "PathFollower.DriveArc.VPGFail",
    359: "PathFollower.DriveArc",
    97: "PathFollower.DrivePointTurn.NegativeFraction",
    360: "PathFollower.DrivePointTurn.VPGFail",
    361: "PathFollower.DrivePointTurn",
    285: "PAP.StartBackingOut.InvalidAction",
    286: "PAP.StartBackingOut.Dist",
    14: "PAP",
    287: "PAP.SET_LIFT_PREDOCK.InvalidAction",
    363: "PAP.DOCKING.DockingFailed",
    289: "PAP.DOCKING.InvalidAction",
    290: "PAP.SET_LIFT_POSTDOCK.InvalidAction",
    291: "PAP.MOVING_LIFT_POSTDOCK.InvalidAction",
    295: "PAP.Update.InvalidAction",
    296: "PAP.DockToBlock.Action",
    297: "PAP.SetRollActionParams",
    1233: "ProxSensors.GetRawCliffValue.InvalidIndex",
    1208: "ProxSensors.UpdateCliff.CliffData",
    339: "ProxSensors.UpdateCliff.StoppingDueToCliff",
    340: "ProxSensors.EnableCliffDetector",
    341: "ProxSensors.EnableStopOnCliff",
    416: "ProxSensors.SetCliffDetectThreshold.TooHigh",
    417: "ProxSensors.SetCliffDetectThreshold.NewLevel",
    239: "SteeringController.SetGains",
    125: "SteeringController.SetPointTurnGains",
    240: "SteeringController.Manage.Mode",
    11: "SteeringController",
    241: "SteeringController.RunLineFollowControllerNL.Errors",
    242: "SteeringController.RunLineFollowControllerNL.Speeds",
    183: "DIRECT DRIVE",
    243: "SteeringController.ExecutePointTurn_Internal.PointTurnTooSlow",
    374: "SteeringController.ExecutePointTurn_2.Params",
    401: "SteeringController.ExecutePointTurn_2.NanParamFound",
    244: "SteeringController.ExecutePointTurn_2.PointTurnTooFast",
    372: "SteeringController.ExitPointTurn",
    1204: "SteeringController.ExecutePointTurn.Params",
    402: "SteeringController.ExecutePointTurn.NanParamFound",
    245: "SteeringController.ExecutePointTurn.PointTurnTooFast",
    246: "SteeringController.ExecutePointTurn.AlreadyAtDest",
    247: "SteeringController.ManagePointTurn.InRange",
    248: "SteeringController.ManagePointTurn.Stopping",
    249: "SteeringController.ManagePointTurn.OOR",
    250: "SteeringController.ManagePointTurn.StoppingCuzStuck",
    1231: "SteeringController.ManagePointTurn.Controller",
    131: "PointTurnSpeed",
    251: "SteeringController.ManagePointTurn.DistToTarget",
    252: "SteeringController.ManagePointTurn.StoppingBecause0Vel",
    63: "TestModeController.Reset",
    64: "TestModeController.PlaceOnGroundTestInit",
    408: "TestModeController.PlaceOnGroundTestUpdate.Complete",
    66: "TestModeController.DockPathTestInit",
    67: "TestModeController.DockPathTestUpdate",
    68: "TestModeController.PathFollowTestInit",
    69: "TestModeController.PathFollowTestUpdate.Complete",
    70: "TestModeController.PathFollowConvenienceFuncTestInit",
    71: "TestModeController.PathFollowConvenienceFuncTestUpdate.DriveStraight",
    72: "TestModeController.PathFollowConvenienceFuncTestUpdate.DriveArc",
    73: "TestModeController.PathFollowConvenienceFuncTestUpdate.DrivePointTurn",
    74: "TestModeController.DriveTestInit",
    75: "TestModeController.DriveTestUpdate",
    76: "TestModeController.LiftTestInit",
    77: "TestModeController.LiftTestUpdate",
    78: "TestModeController.LiftToggleTestInit",
    79: "TestModeController.LiftToggleTestUpdate",
    80: "TestModeController.HeadTestInit",
    81: "TestModeController.HeadTestUpdate",
    82: "TestModeController.IMUTestInit",
    83: "TestModeController.IMUTestUpdate",
    84: "TestModeController.LightTestInit",
    85: "TestModeController.LightTestUpdate",
    88: "TestModeController.StopTestInit",
    89: "TestModeController.StopTestUpdate",
    90: "TestModeController.MaxPowerTestInit",
    91: "TestModeController.MaxPowerTestUpdate",
    92: "TestModeController.Start",
    396: "timeprofiler.getprofname_while_busy",
    397: "timeprofiler.computestats_while_busy",
    31: "VPG",
    232: "VPG.StartProfile_fixedDuration.AccDurationsExceedTotal",
    233: "VPG.StartProfile_fixedDuration.EndPosReachedDuringStartingAcc",
    234: "VPG.StartProfile_fixedDuration.NegativeDiscriminant",
    235: "VPG.StartProfile_fixedDuration.NegativeVm",
    236: "VPG.StartProfile_fixedDuration.VelExceedsMax",
    237: "VPG.StartProfile_fixedDuration.AccelMaxExceeded",
    238: "VPG.Step",
    326: "WheelController.SetGains",
    13: "WheelController",
    143: "Camera.CameraSetParameters",
    1213: "head_timestamp_mismatch",
    128: "Spine.Enqueue.MessageTooLong",
    138: "Spine.Manage",
    406: "WiFi.RadioSendMessage",
    41: "WiFi",
    398: "wifi.dropped_incomming_messages",
    141: "WiFi.Update",
    405: "wifi.update.spine_spin",
    409: "macaddr.soft_ap",
    410: "macaddr.soft_ap.error",
    411: "boot_count.phase",
    412: "boot_count.error",
    413: "client.connections_since_boot",
    1203: "hardware.revision",
    51: "BackgroundTask.IntervalTooLong",
    185: "I2SPI.TooMuchDrift",
    370: "client.reliable_message_dropped",
    403: "I2SPI.Error",
    52: "BackgroundTask.RunTimeTooLong",
    371: "I2SPI.Resync",
    208: "CrashReporter.PutRtipCrashLog.NULL",
    209: "CrashReporter.PutRtipCrashLog.Failed",
    210: "CrashReporter.PutBodyCrashLog.NULL",
    211: "CrashReporter.PutBodyCrashLog.Failed",
    206: "CrashReporter.UnknownReporter",
    207: "CrashReporter.FailedToSend",
    212: "CrashRecorder.AcceptBodyStorage.NoMem",
    197: "Face.Draw.Copy.TooWide",
    213: "Face.Draw.Number.TooWide",
    376: "Face.Draw.NumberTiny.TooWide",
    214: "Face.Draw.Print.TooWide",
    1234: "face_animate.dropped_frame",
    144: "ReliableTransport.SetConnectionTimeout",
    137: "WiFi.Messages",
    364: "WiFi.Messages.ProcessMessage.AddressedToEngine",
    365: "WiFi.Messages.ProcessMessage.TooBig",
    30: "RTIP.SendMessage.TooBig",
    216: "RTIP.SendMessage.Failed",
    50: "RTIP.AcceptRTIPMessage",
    170: "UpdateController",
    171: "UpgradeController",
    172: "UpgradeController.state",
    188: "UpgradeController.termination",
    199: "UpgradeController.encryption.noIV",
    1237: "wifi_telemetry.alloc",
    1192: "IMUCalibration.Read.NotFound",
    1193: "IMUCalibrationData.Read.Success",
    1194: "IMUCalibrationData.Read.NotFound",
    190: "SimHAL.CameraGetFrame.NullFramePointer",
    191: "SimHAL.CameraGetFrame",
    192: "SimHAL.CameraGetFrame.NullImagePointer",
    193: "sim_hal.ReadingDiscoveryChannel.UnexpectedMsg",
    415: "charge_contact_shorted",
    140: "Head.ProcessMessage.BadTag",
    139: "Spine.ProcessMessage"
}

# Map of robot debug format IDs to a tuple (format string, number of arguments).
ROBOT_FORMAT_IDS = {
    0: (
        "Invalid format ID",
        0
    ),
    1: (
        "dropped %d traces",
        1
    ),
    3: (
        "Initializing",
        0
    ),
    612: (
        "Not initializing animation controller because in state %d",
        1
    ),
    4: (
        "Clearing",
        0
    ),
    5: (
        "Failed \"numBytes < KEYFRAME_BUFFER_SIZE\" in file \"supervisor/src/animationController.cpp\" line %d",
        1
    ),
    392: (
        "Message size header (%d) greater than available bytes (%d), assuming corrupt and clearing",
        2
    ),
    393: (
        "Clad message size (%d) doesn't match stored header (%d), assuming corrupt and clearing",
        2
    ),
    477: (
        "BufferKeyFrame called while disabled",
        0
    ),
    6: (
        "BufferKeyFrame.BufferFull %d bytes available, %d needed.",
        2
    ),
    7: (
        "BufferKeyFrame, %d -> %d (%d)",
        3
    ),
    8: (
        "Failed \"numBytesNeeded < KEYFRAME_BUFFER_SIZE\" in file \"supervisor/src/animationController.cpp\" line %d",
        1
    ),
    9: (
        "Failed \"_lastBufferPos >= 0 && _lastBufferPos < KEYFRAME_BUFFER_SIZE\" in file "
        "\"supervisor/src/animationController.cpp\" line %d",
        1
    ),
    11: (
        "Failed \"_currentFrame <= _lastFrame\" in file \"supervisor/src/animationController.cpp\" line %d",
        1
    ),
    620: (
        "Unexpected msgID=%d",
        1
    ),
    455: (
        "Expecting either audio sample or silence next in animation buffer. (Got 0x%02x instead)",
        1
    ),
    451: (
        "Ran out of animation buffer after getting audio/silence.",
        0
    ),
    454: (
        "StartOfAnimation w/ tag=%d",
        1
    ),
    17: (
        "(t=%dms(%d)) tag %d hit EndOfAnimation",
        3
    ),
    18: (
        "(t=%dms(%d)) requesting head angle of %ddeg over %.2fsec",
        4
    ),
    19: (
        "(t=%dms(%d)) requesting lift height of %dmm over %.2fsec",
        4
    ),
    20: (
        "(t=%dms(%d)) setting backpack LEDs.",
        2
    ),
    21: (
        "(t=%dms(%d)) setting face frame.",
        2
    ),
    456: (
        "(t=%dms(%d)) event %d.",
        3
    ),
    24: (
        "(t=%dms(%d)) setting body motion to radius=%d, speed=%d",
        4
    ),
    636: (
        "(t=%dms(%d))",
        2
    ),
    637: (
        "(t=%dms(%d)) turning to recorded heading with offset %d at speed=%d, accel=%d, decel=%d",
        6
    ),
    478: (
        "Unexpected message type %d in animation buffer!",
        1
    ),
    281: (
        "Failed \"_haveReceivedTerminationFrame > 0\" in file \"supervisor/src/animationController.cpp\" line %d",
        1
    ),
    26: (
        "Reached animation %d termination frame (%d frames still buffered, curPos/lastPos = %d/%d).",
        4
    ),
    347: (
        "%d",
        1
    ),
    650: (
        "CompressAndSendImage returned failure (%d)",
        1
    ),
    400: (
        "Setting docking method: %d",
        1
    ),
    634: (
        "H: %f, V: %f",
        2
    ),
    568: (
        "%d ms",
        1
    ),
    569: (
        "(%f > %d)",
        2
    ),
    570: (
        "time=%d, x_distErr=%f, y_horErr=%f, z_height=%f, angleErr=%fdeg",
        5
    ),
    571: (
        "(%f < %d) mode:%i",
        3
    ),
    572: (
        "currTime %d, lastErrSignal %d, Giving up.",
        2
    ),
    573: (
        "currTime %d, lastErrSignal %d, Looking for block...",
        2
    ),
    574: (
        "MaxRetries %d",
        1
    ),
    638: (
        "vert:%f hort:%f rel_x:%f rel_y:%f t:%d",
        5
    ),
    576: (
        "x: %f, y: %f, rad: %f",
        3
    ),
    577: (
        "dockOffsetDistX = %f",
        1
    ),
    578: (
        "HistPose %f %f %f (t=%d), currPose %f %f %f (t=%d)",
        8
    ),
    579: (
        "%f %f %f",
        3
    ),
    431: (
        "Marker is expected to be out of FOV. Ignoring error signal.",
        0
    ),
    472: (
        "Computing straight line path (%f, %f) to (%f, %f)",
        4
    ),
    92: (
        "HEAD FILT: speed %f, speedFilt %f, currentAngle %f, currHalPos %f, prevPos %f, pwr %f",
        6
    ),
    93: (
        "Already at desired angle %f degrees",
        1
    ),
    94: (
        "(fixedDuration): SetDesiredAngle %f rads (duration %f)",
        2
    ),
    95: (
        "(fixedDuration): Already at desired position",
        0
    ),
    616: (
        "startVel %f, startPos %f, acc_start_frac %f, acc_end_frac %f, endPos %f, duration %f. "
        "Trying VPG without fixed duration.",
        6
    ),
    97: (
        "VPG (fixedDuration): startVel %f, startPos %f, acc_start_frac %f, acc_end_frac %f, endPos %f, duration %f",
        6
    ),
    299: (
        "Recalibrating (power = %f)",
        1
    ),
    98: (
        "HEAD ANGLE REACHED (%f rad)",
        1
    ),
    564: (
        "New head gains: kp = %f, ki = %f, kd = %f, maxSum = %f",
        4
    ),
    604: (
        "acc (%f, %f, %f), gyro (%f, %f, %f), cliff %d",
        7
    ),
    629: (
        "accX %f, accY %f, accZ %f, cliff %d, gyroZ %d",
        5
    ),
    166: (
        "Max gyro: %f %f %f",
        3
    ),
    483: (
        "%f deg (motion %d, gyro %f)",
        3
    ),
    584: (
        "time %dms",
        1
    ),
    585: (
        "time = %dms",
        1
    ),
    308: (
        "LIFT FILT: speed %f, speedFilt %f, currentAngle %f, currHalPos %f, prevPos %f, pwr %f",
        6
    ),
    145: (
        "Already at desired height %f",
        1
    ),
    146: (
        "LIFT DESIRED HEIGHT: %f mm (curr height %f mm), duration = %f s",
        3
    ),
    148: (
        "VPG (fixedDuration): startVel %f, startPos %f, acc_start_frac %f, acc_end_frac %f, endPos %f, duration %f",
        6
    ),
    628: (
        "in %d ms",
        1
    ),
    152: (
        "LIFT HEIGHT REACHED (%f mm)",
        1
    ),
    613: (
        "LIFT: currA %f, curDesA %f, currVel %f, desA %f, err %f, errSum %f, inPos %d",
        7
    ),
    614: (
        "P: %f, I: %f, D: %f, total: %f",
        4
    ),
    563: (
        "New lift gains: kp = %f, ki = %f, kd = %f, maxSum = %f",
        4
    ),
    300: (
        "pose2 is older than pose1",
        0
    ),
    301: (
        "targetTime is outside expected range",
        0
    ),
    302: (
        "x= %f, y= %f, angle= %f",
        3
    ),
    303: (
        "Couldn't find timestamp %d in history (oldest(%d) %d, newest(%d) %d)",
        5
    ),
    304: (
        "Ignoring keyframe %d at time %d",
        2
    ),
    306: (
        "History starts at time %d, pose requested at time %d. Returning oldest pose.",
        2
    ),
    307: (
        "History ends at time %d, pose requested at time %d. Returning newest pose.",
        2
    ),
    355: (
        "Received message with bad tag %x",
        1
    ),
    356: (
        "Timed out waiting for message ID %d.",
        1
    ),
    363: (
        "Result %d, currTime=%d, updated frame time=%d: (%.3f,%.3f) at %.1f degrees (frame = %d)",
        7
    ),
    630: (
        "action %d, dockMethod %d, doLiftLoadCheck %d, speed %f, acccel %f, decel %f, manualSpeed %d",
        7
    ),
    364: (
        "left=%f mm/s, right=%f mm/s",
        2
    ),
    357: (
        "height %f, maxSpeed %f, duration %f",
        3
    ),
    365: (
        "angle %f, maxSpeed %f, duration %f",
        3
    ),
    366: (
        "speed %f rad/s, accel %f rad/s2",
        2
    ),
    358: (
        "mode: %d, resolution: %d",
        2
    ),
    362: (
        "controller: %d",
        1
    ),
    449: (
        "enabled: %d, liftPower: %f, headPower: %f",
        3
    ),
    367: (
        "Receiver got %02x(%d) invalid",
        2
    ),
    368: (
        "Parsed message size error %d != %d",
        2
    ),
    369: (
        "ReliableTransport new connection",
        0
    ),
    370: (
        "ReliableTransport connection completed",
        0
    ),
    371: (
        "ReliableTransport disconnected",
        0
    ),
    359: (
        "NULL HeadCamInfo retrieved from HAL.",
        0
    ),
    611: (
        "operation=%d",
        1
    ),
    275: (
        "Failed \"false\" in file \"supervisor/src/path.cpp\" line %d",
        1
    ),
    538: (
        "(%f, %f) to (%f, %f), speed/accel/decel = (%f, %f, %f)",
        7
    ),
    539: (
        "centerPt (%f, %f), radius %f, startAng %f, sweep %f, speed/accel/decel = (%f, %f, %f)",
        8
    ),
    540: (
        "x %f, y %f, targetAngle %f, speed/accel/decel = (%f, %f, %f)",
        6
    ),
    541: (
        "LINE (%f, %f) (%f, %f)",
        4
    ),
    542: (
        "Robot Pose: x: %f, y: %f ang: %f",
        3
    ),
    543: (
        "m: %f, b: %f",
        2
    ),
    544: (
        "x_int: %f, y_int: %f, b_inv: %f",
        3
    ),
    545: (
        "dy: %f, dx: %f, dist: %f",
        3
    ),
    546: (
        "signbit(dx): %d, dy_sign: %f",
        2
    ),
    547: (
        "lineTheta: %f",
        1
    ),
    60: (
        "lineTheta: %f, robotTheta: %f",
        2
    ),
    548: (
        "center (%f, %f), startRad: %f, sweepRad: %f, radius: %f",
        5
    ),
    551: (
        "x: %f, y: %f, m: %f, b: %f",
        4
    ),
    552: (
        "x_center: %f, y_center: %f",
        2
    ),
    553: (
        "x_int: %f, y_int: %f",
        2
    ),
    554: (
        "dy: %f, dx: %f, dist: %f, radDiff: %f",
        4
    ),
    555: (
        "insideCircle: %d, segmentRangeStatus: %d",
        2
    ),
    556: (
        "theta_line: %f, theta_tangent: %f",
        2
    ),
    557: (
        "center (%f, %f), targetAngle: %f, targetRotSpeed: %f",
        4
    ),
    276: (
        "Failed \"capacity_ == rhs.capacity_\" in file \"supervisor/src/path.cpp\" line %d",
        1
    ),
    277: (
        "Failed \"capacity_ == MAX_NUM_PATH_SEGMENTS\" in file \"supervisor/src/path.cpp\" line %d",
        1
    ),
    558: (
        "Path segment %d - ",
        1
    ),
    278: (
        "Failed \"pathType != NUM_DUBINS_PATHS\" in file \"supervisor/src/path.cpp\" line %d",
        1
    ),
    72: (
        "Dubins %d: p_c1 (%f, %f) p_c2 (%f, %f)",
        5
    ),
    73: (
        "V1 (%f %f)  n (%f %f)  p_t1 (%f, %f)  p_t2 (%f, %f)",
        8
    ),
    74: (
        "DUBINS: startPt %f %f %f, preEnd %f %f, endPt %f %f %f, start_radius %f, end_radius %f",
        10
    ),
    75: (
        "Dubins path %d: numSegments %d, length %f m",
        3
    ),
    279: (
        "Failed \"0\" in file \"supervisor/src/path.cpp\" line %d",
        1
    ),
    77: (
        "Dubins: Shortest path %d, length %f",
        2
    ),
    78: (
        "WARNING(Path::PopFront): Can't pop %d segments from %d segment path",
        2
    ),
    79: (
        "WARNING(Path::PopBack): Can't pop %d segments from %d segment path",
        2
    ),
    559: (
        "Segment %d greater than number of segments %d",
        2
    ),
    560: (
        "Segment %d start point (%f, %f), Segment %d end point (%f, %f)",
        6
    ),
    561: (
        "MAX_NUM_PATH_SEGMENTS: %d",
        1
    ),
    562: (
        "numPathSegments_ = %u",
        1
    ),
    286: (
        "Failed \"path_.GetNumSegments() > 0\" in file \"supervisor/src/pathFollower.cpp\" line %d",
        1
    ),
    586: (
        "%f  (res=%d)",
        2
    ),
    587: (
        "New closest seg: %d, distToSegment %f (res=%d)",
        3
    ),
    588: (
        "Start segment %d, speed = %f, accel = %f, decel = %f",
        4
    ),
    287: (
        "Failed \"Planning::PST_LINE == path_(currPathSegment_).GetType() || Planning::PST_ARC == "
        "path_(currPathSegment_).GetType()\" in file \"supervisor/src/pathFollower.cpp\" line %d",
        1
    ),
    219: (
        "PathFollower: Decel to end of segment %d (of %d) at %d mm/s^2 from speed of %d mm/s (meas %d mm/s) over %f mm",
        6
    ),
    589: (
        "currCmdSpeed %d mm/s, currSpeed %d mm/s)",
        2
    ),
    590: (
        "currPathSeg: %d, TURN currAngle: %f, targetAngle: %f",
        3
    ),
    591: (
        "Segment %d has invalid type %d",
        2
    ),
    592: (
        "%f mm, %f deg, segRes %d, segType %d, currSeg %d",
        5
    ),
    593: (
        "Segment %d, speed = %f, accel = %f, decel = %f",
        4
    ),
    594: (
        "%f mm",
        1
    ),
    349: (
        "start: %f, end: %f",
        2
    ),
    595: (
        "total dist %f, startDist %f, endDist %f",
        3
    ),
    596: (
        "start %f, end %f, vel %f",
        3
    ),
    597: (
        "(%f, %f) to (%f, %f) to (%f, %f) to (%f, %f)",
        8
    ),
    598: (
        "curr_x,y  (%f, %f), center x,y (%f, %f), radius %f",
        5
    ),
    599: (
        "start + sweep1 = ang1 (%f + %f = %f), end + sweep2 = ang2 ang2 (%f - %f = %f)",
        6
    ),
    600: (
        "targetSpeed %f, startAccel %f, endAccel %f",
        3
    ),
    601: (
        "sweep_rad: %f, acc_start_frac %f, acc_end_frac %f, duration_sec %f",
        4
    ),
    602: (
        "start %f, int_ang1 %f, int_ang2 %f, dest %f",
        4
    ),
    603: (
        "targetRotSpeed %f, startRotAccel %f, endRotAccel %f",
        3
    ),
    565: (
        "Starting %.1fmm backout (%.2fsec duration)",
        2
    ),
    120: (
        "SETTING LIFT PREDOCK (action %d)",
        1
    ),
    122: (
        "DOCKING",
        0
    ),
    123: (
        "ALIGN",
        0
    ),
    124: (
        "TRAVERSE_RAMP_DOWN",
        0
    ),
    125: (
        "ENTER_BRIDGE",
        0
    ),
    127: (
        "SET_LIFT_POSTDOCK",
        0
    ),
    131: (
        "SETTING LIFT POSTDOCK",
        0
    ),
    134: (
        "Switching out of TRAVERSE_RAMP_DOWN to TRAVERSE_RAMP (angle = %f)",
        1
    ),
    135: (
        "IDLE (from TRAVERSE_RAMP)",
        0
    ),
    136: (
        "TRAVERSE_BRIDGE",
        0
    ),
    137: (
        "LEAVING_BRIDGE: relMarkerX = %f",
        1
    ),
    138: (
        "TRAVERSE_BRIDGE: Restarting tracking",
        0
    ),
    139: (
        "IDLE (from TRAVERSE_BRIDGE)",
        0
    ),
    567: (
        "liftHeight: %f, speed: %f, accel: %f, duration %d, backupDist %f",
        5
    ),
    647: (
        "Index %d is not valid",
        1
    ),
    635: (
        "raw: %d, off: %d, thresh: %d / %d",
        4
    ),
    282: (
        "Failed \"!NEAR_ZERO(b)\" in file \"supervisor/src/radians.cpp\" line %d",
        1
    ),
    529: (
        "New gains: k1 %f, k2 %f, dist_cap %f mm, ang_cap %f rad",
        4
    ),
    373: (
        "New gains: kp %f, ki %f, kd %f, maxSum %f",
        4
    ),
    105: (
        "Wheel speed adjust: (%f, %f), adjustment %f",
        3
    ),
    530: (
        "offsetError_mm: %f, headingError_rad: %f, curvature: %f, currSpeed: %d",
        4
    ),
    531: (
        "%d (L), %d (R)",
        2
    ),
    484: (
        "%d: %f   %f  (%f %f)",
        5
    ),
    532: (
        "Speeding up commanded point turn of %f rad/s to %f rad/s",
        2
    ),
    610: (
        "%d: vel %f, accel %f",
        3
    ),
    617: (
        "%f, %f",
        2
    ),
    533: (
        "Speed of %f deg/s exceeds limit of %f deg/s. Clamping.",
        2
    ),
    633: (
        "%d: target %f, vel %f, accel %f, decel %f, tol %f, shortestDir %d, numHalfRevs %d",
        8
    ),
    618: (
        "%f, %f, %f, %f, %f",
        5
    ),
    534: (
        "distToTarget %f, currAngle %f, currDesired %f (currTime %d, inPosTime %d)",
        5
    ),
    535: (
        "currAngle %f, currDesired %f, currVel %f, distTraversed %f, distExpected %f, "
        "wheelSpeeds %f %f, desSpeeds %f %f",
        9
    ),
    536: (
        "currAngle %f, currDesired %f",
        2
    ),
    643: (
        "timestamp %d, currAngle %.1f, desAngle %.1f, currSpeed %.1f, desSpeed %.1f, "
        "arcVel %d, ff %.1f, p %.1f, i %.1f, d %.1f, errSum %.1f",
        11
    ),
    377: (
        "des %f deg/s, meas: %f deg/s, arcVel %d mm/s, errorSum %f",
        4
    ),
    537: (
        "angularDistToTarget: %f radians, arcVel: %d mm/s",
        2
    ),
    309: (
        "xOffset %d mm, yOffset %d mm, angleOffset %d degrees",
        3
    ),
    311: (
        "Test state: %d",
        1
    ),
    312: (
        "Started",
        0
    ),
    313: (
        "FAILED",
        0
    ),
    314: (
        "%x, %d, %d",
        3
    ),
    315: (
        "Applying %.3f power (currSpeed %.2f %.2f, filtSpeed %.2f %.2f)",
        5
    ),
    316: (
        "Going %.3f mm/s (currSpeed %.2f %.2f, filtSpeed %.2f %.2f)",
        5
    ),
    317: (
        "flags = %d, powerPercent = %d",
        2
    ),
    403: (
        "Lift HIGH %f mm (maxSpeed %f rad/s)",
        2
    ),
    404: (
        "Lift LOW %f mm (maxSpeed %f rad/s)",
        2
    ),
    405: (
        "Lift UP %f power (maxSpeed %f rad/s)",
        2
    ),
    434: (
        "Lift DOWN %f power (maxSpeed %f rad/s)",
        2
    ),
    322: (
        "WARN: Unknown lift test mode %d",
        1
    ),
    323: (
        "Avg lift speed %f rad/s, height change %f mm",
        2
    ),
    324: (
        "SET LIFT TO %f mm",
        1
    ),
    325: (
        "Lift speed %f rad/s, height %f mm",
        2
    ),
    407: (
        "Head HIGH %f rad (maxSpeed %f rad/s)",
        2
    ),
    408: (
        "Head LOW %f rad (maxSpeed %f rad/s)",
        2
    ),
    409: (
        "Head UP %f power (maxSpeed %f rad/s)",
        2
    ),
    410: (
        "Head DOWN %f power (maxSpeed %f rad/s)",
        2
    ),
    330: (
        "Unknown head test mode %d",
        1
    ),
    331: (
        "Head speed %f rad/s (filt %f rad/s), angle %f rad",
        3
    ),
    332: (
        "Turning to 180",
        0
    ),
    333: (
        "Turning to 0",
        0
    ),
    334: (
        "Gyro (%f,%f,%f) rad/s, (%f,%f,%f) mm/s^2",
        6
    ),
    335: (
        "Rot(IMU): %f deg",
        1
    ),
    336: (
        "flags = %x, ledID = %d, color = %x",
        3
    ),
    337: (
        "LED channel %d, color 0x%x",
        2
    ),
    340: (
        "GO: %f mm/s",
        1
    ),
    341: (
        "STOPPED: (%f, %f) mm in %d tics",
        3
    ),
    342: (
        "SWITCHING POWER: %f",
        1
    ),
    344: (
        "Undefined test mode %d",
        1
    ),
    280: (
        "Failed \"timeProfIdx_ < MAX_NUM_PROFILES\" in file \"supervisor/src/timeProfiler.cpp\" line %d",
        1
    ),
    27: (
        "GetProfName called in middle of profile. Ignoring.",
        0
    ),
    28: (
        "ComputeStats called in middle of profile. Ignoring.",
        0
    ),
    254: (
        "Failed \" !(y == 0 && x == 0)\" in file \"supervisor/src/trig_fast.cpp\" line %d",
        1
    ),
    255: (
        "Failed \"y != 0 || x != 0\" in file \"supervisor/src/trig_fast.cpp\" line %d",
        1
    ),
    283: (
        "Failed \"maxVel_ >= endVel_\" in file \"supervisor/src/velocityProfileGenerator.cpp\" line %d",
        1
    ),
    284: (
        "Failed \"accel_ > 0\" in file \"supervisor/src/velocityProfileGenerator.cpp\" line %d",
        1
    ),
    285: (
        "Failed \"timeStep_ > 0\" in file \"supervisor/src/velocityProfileGenerator.cpp\" line %d",
        1
    ),
    200: (
        "new V_max: %f (d = %f)",
        2
    ),
    201: (
        "startVel %f, startPos %f, maxSpeed %f, accel %f",
        4
    ),
    202: (
        "endVel %f, endPos %f, timestep %f",
        3
    ),
    203: (
        "deltaVel %f, maxReachableVel %f, totalDist %f, decelDistToTarget %f, dir %f",
        5
    ),
    522: (
        "acc_start_duration + acc_end_duration exceeds total duration (%f + %f > %f)",
        3
    ),
    524: (
        "A = %f, B = %f, C = %f",
        3
    ),
    525: (
        "vm > 0  (A = %f, B = %f, C = %f)",
        3
    ),
    526: (
        "vs = %f, vm = %f, vel_max = %f",
        3
    ),
    527: (
        "acc_start = %f, acc_end = %f, acc_max = %f",
        3
    ),
    210: (
        "startVel %f, startPos %f, endVel %f, endPos %f",
        4
    ),
    211: (
        "ts %f, tm %f, te %f, total duration %f",
        4
    ),
    212: (
        "deltaVelStart %f, deltaVelEnd %f, maxReachableVel %f",
        3
    ),
    213: (
        "totalDist %f, decelDistToTarget %f",
        2
    ),
    378: (
        "Failed \"maxReachableVel_ == endVel_\" in file \"supervisor/src/velocityProfileGenerator.cpp\" line %d",
        1
    ),
    528: (
        "currVel %f, currPos %f, currDistToTarget %f, isDecel %d",
        4
    ),
    580: (
        "New gains: kp=%f, ki=%f, maxSum=%f",
        3
    ),
    115: (
        "speeds: %f (L), %f (R)   (Curr: %d, %d)",
        4
    ),
    116: (
        "desired speeds: %f (L), %f (R)",
        2
    ),
    117: (
        "error: %f (L), %f (R)   error_sum: %f (L), %f (R)",
        4
    ),
    118: (
        "power: %f (L), %f (R)",
        2
    ),
    395: (
        "Clipping exposure of %dms to %dms",
        2
    ),
    639: (
        "Timestamp expected: %d, got %d",
        2
    ),
    382: (
        "Message %x(%d) is too long to enqueue to body. MAX_SIZE = %d",
        3
    ),
    383: (
        "Received message %x(%d) that seems bound below",
        2
    ),
    390: (
        "Received message %x has %d bytes but should have %d",
        3
    ),
    619: (
        "Refusing to send message %x(%d) to self!",
        2
    ),
    260: (
        "Can't send message %x(%d) to WiFi, max size %d",
        3
    ),
    615: (
        "%d messages dropped, tick %d, time %d, buffer %x %x %d",
        6
    ),
    380: (
        "Got message 0x%x that seems bound above.",
        1
    ),
    621: (
        "Spun %d times",
        1
    ),
    381: (
        "CLAD message 0x%x size %d doesn't match size in buffer %d",
        3
    ),
    624: (
        "%02x:%02x:%02x:%02x:%02x:%02x",
        6
    ),
    625: (
        "Unable to retrieve softap MAC address",
        0
    ),
    626: (
        "%x",
        1
    ),
    627: (
        "Unable to retrieve boot phase indicator",
        0
    ),
    632: (
        "Hardware 1.%d",
        1
    ),
    295: (
        "Background task interval too long: %dus!",
        1
    ),
    486: (
        "TMD=%d\\tintegral=%d",
        2
    ),
    607: (
        "count = %d",
        1
    ),
    622: (
        "code=%x, data=%x",
        2
    ),
    296: (
        "Background task %d run time too long: %dus!",
        2
    ),
    608: (
        "I2SPI resynchronizing",
        0
    ),
    515: (
        "RTIP Crash log pointer is null",
        0
    ),
    516: (
        "Failed to put crash record %d",
        1
    ),
    517: (
        "Body Crash log pointer is null",
        0
    ),
    513: (
        "Reporter = %d",
        1
    ),
    514: (
        "Couldn't send crash report, will retry.",
        0
    ),
    518: (
        "Couldn't allocate memory for RTIP crash log",
        0
    ),
    519: (
        "Couldn't allocate memory for body crash log",
        0
    ),
    520: (
        "%d + %d > %d",
        3
    ),
    648: (
        "Dropping frame because %d rects remaining",
        1
    ),
    399: (
        "Timeout is now %dms",
        1
    ),
    259: (
        "Received message not expected here tag=%02x",
        1
    ),
    394: (
        "ToRobot message %x(%d) like like it has tag for engine (> 0x%x)",
        3
    ),
    256: (
        "Received message too big! %02x(%d) > %d",
        3
    ),
    258: (
        "Failed to buffer a keyframe! Clearing Animation buffer!",
        0
    ),
    198: (
        "SendMessage: Message too large for RTIP, %d > %d",
        2
    ),
    199: (
        "SendMessage: Couldn't forward message %x(%d) to RTIP. I2SPI mode = %d",
        3
    ),
    415: (
        "SendMessage with %x(%d) > %d",
        3
    ),
    376: (
        "WiFi received message from RTIP, %x(%d) that seems bound below (< 0x%x)",
        3
    ),
    442: (
        "dropping RTIP trace",
        0
    ),
    289: (
        "Couldn't relay message (%x(%d)) from RTIP over wifi",
        2
    ),
    466: (
        "Reset()",
        0
    ),
    467: (
        "Received termination",
        0
    ),
    468: (
        "flash erase",
        0
    ),
    469: (
        "sync recovery",
        0
    ),
    470: (
        "Flash Verify",
        0
    ),
    457: (
        "Apply Wifi",
        0
    ),
    489: (
        "No valid certificate!",
        0
    ),
    507: (
        "no IV!",
        0
    ),
    508: (
        "Flash Decrypt",
        0
    ),
    509: (
        "Flash Write",
        0
    ),
    490: (
        "Sig Check",
        0
    ),
    491: (
        "Unhandled special block 0x%x",
        1
    ),
    461: (
        "Flash verify",
        0
    ),
    499: (
        "Flash wait",
        0
    ),
    463: (
        "Reboot",
        0
    ),
    462: (
        "Wait for RTIP Ack",
        0
    ),
    464: (
        "Wait for reboot",
        0
    ),
    465: (
        "Failed \"false\" in file \"espressif/app/application/upgradeController.cpp\" line %d",
        1
    ),
    651: (
        "Couldn't allocate memory for time",
        0
    ),
    652: (
        "Couldn't allocate memory for debug packet",
        0
    ),
    501: (
        "No IMU calibration data available",
        0
    ),
    502: (
        "Got calibration data: gyro={%d, %d, %d}, acc={%d, %d, %d}",
        6
    ),
    503: (
        "No IMU calibration data written",
        0
    ),
    494: (
        "NULL frame pointer provided to CameraGetFrame(), check to make sure the image allocation succeeded.",
        0
    ),
    495: (
        "Image requested too soon -- new frame may not be ready yet.",
        0
    ),
    496: (
        "NULL image pointer returned from simulated camera's getFrame() method.",
        0
    ),
    497: (
        "Expected discovery tag but got %d",
        1
    ),
    385: (
        "Message to body, unhandled tag 0x%x",
        1
    ),
    384: (
        "Body received message %x that seems bound above",
        1
    ),
    386: (
        "Message %x(%d) too long to enqueue to head. MAX_SIZE = %d",
        3
    )
}


def get_log_level(robot_level: int) -> int:
    """ Translate robot log level to Python log level. """
    return ROBOT_LOG_LEVELS.get(robot_level, logging.DEBUG)


def get_debug_message(name_id: int, format_id: int, args: List[Any]) -> Optional[str]:
    """ Generate a log message from robot debug name and format IDs. """
    fmt = ROBOT_FORMAT_IDS.get(format_id)
    if fmt:
        if fmt[1]:
            assert fmt[1] == len(args)
            msg = (fmt[0] % tuple(args))    # noqa
        else:
            msg = fmt[0]
    else:
        msg = ""
    name = ROBOT_NAME_IDS.get(name_id)
    if name:
        if msg:
            msg = "{}: {}".format(name, msg)
        else:
            msg = name
    return msg
