Cozmo Functions
===============


Overview
--------

Cozmo is a complex distributed embedded system with the following main parts:

- robot
- cubes
- charging platform 

The robot can be subdivided into:

- head
    - Wi-Fi communication controller ([Espressif ESP8266](https://en.wikipedia.org/wiki/ESP8266))
    - Real-time and Image Processing (RTIP) controller ([NXP Kinetis K02](https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/k-series-cortex-m4/k0x-entry-level/kinetis-k02-100-mhz-microcontrollers-mcus-with-optimized-features-based-on-arm-cortex-m4-core:K02_100))
- body
    - Body controller ([Nordic nRF51822](https://www.nordicsemi.com/Products/Low-power-short-range-wireless/nRF51822))

The Wi-Fi communication controller is responsible for the following functions:
- Wi-Fi communication
- over-the-air (OTA) firmware updates
- NV RAM storage

Once Cozmo is powered on, the communications controller remains always powered on to maintain Wi-Fi communication. 

On connection, the robot transmits its serial number with the `HardwareInfo` message and firmware version with the
`FirmwareSignature` message.

The RTIP controller is responsible for:
- OLED display image decoding
- speaker audio decoding
- camera image encoding
- accelerometers
- gyro

The body controller is in charge of:
- left and right tread motors and encoders encoders
- head motor and encoder
- lift motor and encoder
- backpack LEDs
- backpack button (on newer models only)
- Bluetooth LE communication (to cubes and charging platform)
- IR LED
- cliff sensor
- batter charging

The body is powered on with the `Enable` message. The `BodyInfo` message communicates the body hardware version, 
serial number, and color.

Cubes use Nordic nRF31512 MCU. They are communicated with over Bluetooth LE and provide access to:
- LEDs
- Accelerometers
- Battery voltage

Some charging platforms (aka "pads") can be communicated with over Bluetooth LE. They contains 3 RGB LEDs that can be
controlled, similar to cube LEDs.

The following sections provide more details on the use of each function.


Wi-Fi
-----

Wi-Fi is activated automatically when the head board is powered on. The robot operates in access point (AP) mode.

`cozmoclad` defines a `SetBodyRadioMode` message that seems to allow changing the Wi-Fi channel but it is unclear
how it can be used with the Cozmo protocol.

`WifiOff`
`Shutdown`


Backpack LEDs
-------------

The 5 Backpack LEDs can be set controlled with 2 messages:
- `lightStateCenter` - controls the top, middle, and bottom RGB LEDs.
- `LightStateSide` - controls the left and right red-only LEDs.

Each color is defined by a 5-bit value for a total of 32768 colors.

See `examples/backpack_lights.py` for example usage.


Backpack Button
---------------

v1.5 and newer Cozmo models have a backpack button. 

Button press and release events are communicated by the `ButtonPressed` message. It is immediately available on
connection and does not require `Enable` to be used.

The `RobotState` message has a `backpack_touch_sensor_raw` field but
it seems that it's value does not change as a result of button presses.

See `examples/events.py` for example usage.


Wheels
------

The left and the right motor speeds can be controlled directly using the `DriveWheels` and `TurnInPlaceAtSpeed`
messages. The motors can be stopped using the `StopAllMotors` message.

The actual speed of wheels is measured with Hall magnetic sensors. The values for each wheel can be
read through the `lwheel_speed_mmps` and `rwheel_speed_mmps` fields of the `RobotState` message.

In addition, the and `TurnInPlace` message can be used to turn to a specific angle.


Localization
------------

The robot maintains a world frame internally. It's position and orientation with respect to it are transmitted every
30 ms or about 33 times per second with the `RobotState` message.

If the robot is unable to maintain correct position and orientation, for example because it is picked up or pushed, it
will communicate this with a `RobotDelocalized` message.

The origin (0,0,0) of the world frame as well as "pose ID" can be set with the `SetOrigin` message. This is usually done
on initial connection and and on receiving a `RobotDelocalized` message.

The timestamp in `RobotState` messages can be synchronized using the `SyncTime` message.


Path Tracking
-------------

The robot can traverse paths, composed of lines, arcs, and turns in place, described in world frame coordinates. The
`AppendPathSegLine`, `AppendPathSegArc`, and `AppendPathSegPointTurn` messages can be used to build paths.

The last composed path can be executed using the `ExecutePath` message. One of it's arguments can be used to request
the reception of  `PathFollowingEvent` message when path traversing finishes.

The `status` filed of the `RobotState` message has a `robot_pathing` flag that indicates whether the robot is currently
traversing a path. The `curr_path_segment` filed indicates which segment is being traversed. 

The `ClearPath` message can be used to destroy an already composed path. The `TrimPath` message can be used to delete
path segments from the beginning or the end of a composed path.

See `examples/path.py` and `examples/go_to_pose.py` for example usage.


Head
----

The head motor can be controlled directly, using the `DriveHead` and `SetHeadAngle` messages. `SetHeadAngle` is always
followed by an `AcknowledgeAction` message before the head starts moving. 

The actual head angle can be read through the `head_angle_rad` field of the `RobotState` message. The `head_in_pos` flag
of the `status` field indicates whether the head is in position or in motion.

The motor can be stopped using the `StopAllMotors` message.

The robot measures the angle of the head, relative to its lowest possible position. This measurement is automatically
triggered on connection. The head can be forced to an unknown angle for example as a result of a fall.
In such situations, the robot recalibrates the head motor automatically. Calibration can also be triggered on request,
using the `StartMotorCalibration` message. The `MotorCalibration` message indicates whether calibration is in progress.

See `examples/extremes.py` for example usage.


Lift
----

The head motor can be controlled directly, using the `DriveLift` and `SetLiftHeight` messages. `SetLiftHeight` is always
followed by an `AcknowledgeAction` message before the lift start moving.

The actual lift height can be read through the `lift_height_mm` field of the `RobotState` message. The `lift_inpos` flag
of the `status` field indicates whether the lift is in position or in motion.

The motor can be stopped using the `StopAllMotors` message.

The robot measures the angle of the lift, relative to its lowest possible position. It is calibrated similar to the
head motor.

See `examples/extremes.py` for example usage.


OLED display
------------

Images can be displayed on the robot's OLED 128x64 display using the `DisplayImage` message. To reduce display burn-in,
consecutive images are interleaved and only half of the display's rows can be used at a time and the effective display
resolution is 128x32.

The Cozmo protocol uses a special run-length encoding to compress images.

Display and audio are synchronized by audio messages (`OutputAudio` and `OutputSilence`). 

`AnimationState` message which can be enabled using the `EnableAnimationState` message provide statistics on display
usage.

See `examples/display_image.py` and `examples/display_lines.py` for example usage.


Speaker
-------

The `OutputAudio` message can be used to transmit 744 audio samples at a time.
The samples are 8-bit and [u-law](https://en.wikipedia.org/wiki/%CE%9C-law_algorithm) encoded.

Speaker volume can be adjusted with the `SetRobotVolume` message.
 
`AnimationState` message which can be enabled using the `EnableAnimationState` message provide statistics on audio
usage.

See `examples/audio.py` for example usage. 


Camera
------

Cozmo can send a stream of camera images in 320x240 (QVGA) resolution at a rate of ~15 frames per second.

The `EnableCamera` message enables camera image reception and the `EnableColorImages` message allows switching between
grayscale and color images.

The camera gain, exposure time, and auto exposure can be controlled with the `SetCameraParams` message.

Images are encoded in JPEG format and transmitted as a series of `ImageChunk` messages. The header of the JPEG files is
not transmitted to save bandwidth.

The `ImageImuData` message provides accelerometer readings at the time of capturing every image to allow for motion
blur compensation.
 
See `examples/camera.py` for example usage. 


IR LED
------

The IR LED (aka head light) can improve the camera performance in dark environments.

The IR LED can be turned on and off using the `SetHeadLight` message.


Accelerometers
--------------

The `RobotState` message communicates accelerometer readings which represent acceleration along the x, y, and z axes.

In addition, the robot automatically detects and communicates 2 types of events. The `RobotPoked` message is sent if 
the robot has been moved rapidly by an external force along the x or y axes. The `FallingStarted` and `FallingStopped`
messages are send if the robot is moving rapidly along the z axis.

See `examples/events.py` for example usage.


Gyro
----

The `RobotState` message communicates gyro readings which represent angular velocity around the x, y, and z axes.

See `examples/events.py` for example usage.


Cliff Sensor
------------

The robot has a "cliff sensor" that measures the distance to ground below the robot. This allows detecting cliffs and
detecting when the robot is being picked up or put down.

The `RobotState` message communicates the raw cliff sensor readings.

In addition, the robot can be made to automatically stop when a cliff is detected with the `EnableStopOnCliff` message.

See `examples/events.py` for example usage.


Battery voltage
---------------

The `RobotState` message communicates raw battery voltage readings.


NV RAM Storage
--------------

The robot provides access to some amount of non-volatile memory (aka NV RAM) intended to store two main types of data:

- unit-specific parameters (ex. camera calibration data and cube IDs) 
- mobile app data (ex. sparks and unlocked games and tricks)
 
The NV RAM storage is backed by the head's ESP8266 controller external SPI flash. It is a NOR flash which drives the
following specifics for its use:

- an erase operation is needed before a write operation
- data is erased in pages

The `NvStorageOp` message allows performing read, erase, and write operations. Data is addressed by the `tag` field and
only the values enumerated by `NvEntryTag` can be used. Using any other address results in a `NV_BAD_ARGS`. Tags
smaller than 0x80000000 are direct NOT flash memory addresses. Tags larger than 0x80000000 are virtual addresses that
seem to be stored in the `NVEntry_FactoryBaseTagWithBCOffset` area.

`NvStorageOpResult` messages communicate results of `NvStorageOp` operations.

A backup through the mobile app, preserves the data behind the following keys:

- NVEntry_GameSkillLevels
- NVEntry_Onboarding
- NVEntry_GameUnlocks
- NVEntry_FaceEnrollData
- NVEntry_FaceAlbumData
- NVEntry_NurtureGameData
- NVEntry_InventoryData
- NVEntry_LabAssignments

See `examples/nvram.py` for example usage.


Firmware Updates
----------------

Cozmo firmware updates are distributed in "cozmo.safe" files that seem to contain firmware images for all three of
Cozmos controllers - the Wi-Fi communication controller, the RTIP controller, and the body controller.

The "cozmo.safe" files start with a firmware signature in JSON format:

```json
{
    "version": 2381,
    "git-rev": "408d28a7f6e68cbb5b29c1dcd8c8db2b38f9c8ce",
    "date": "Tue Jan  8 10:27:05 2019",
    "time": 1546972025,
    "messageEngineToRobotHash": "9e4a965ace4e09d86997b87ba14235d5",
    "messageRobotToEngineHash": "a259247f16231db440957215baba12ab",
    "build": "DEVELOPMENT",
    "wifiSig": "69ca03352e42143d340f0f7fac02ed8ff96ef10b",
    "rtipSig": "36574986d76144a70e9252ab633be4617a4bc661",
    "bodySig": "695b59eff43664acd1a5a956d08c682b3f8bd2c8"
}
```

This is the same signature, delivered with the `FirmwareSignature` message on initial connection establishment.

See `docs/versions.md` for more examples.

There seem to be individual signatures for each controller but the structure of the `cozmo.safe` files is not known.

The firmware image is transferred as-is from the engine to the robot, using `FirmwareUpdate` messages. It is divided
into 1024 B chunks that are numbered consecutively, starting with 0. Each chunk is confirmed by the robot with a
`FirmwareUpdateResult` message with `status` field set to 0.

Firmware transfer completion is indicated by the engine with e `FirmwareUpdate` message with chunk ID set to 0xFFFF and
data set to all-zeros. The robot confirms firmware update completion by sending a `FirmwareUpdateResult` message that
repeats the last chunk ID and has a `status` field set to 10.


Bluetooth LE
------------

"Objects", that can be connected to over Bluetooth LE announce their availability with an `ObjectAvailable` message
periodically. The `ObjectAvailable` message contains the object type (e.g. light cube 1, 2, 3 or charging pad) and
the object factory ID which identifies it uniquely.

The `ObjectConnect` message is used to initiate or terminate a connection to objects, using their factory ID.

Connection establishment and termination is announced with the `ObjectConnectionState` message. It contains a temporary
"object ID" that is used to identify the object for the duration of the connection with it.


Cube LEDs
---------

Cubes have 4 RGB LEDs that can be controlled individually.

A cube has to be "selected" first, using the `CubeId` message. A subsequent `CubeLights` message sets the state of all
4 cube LEDs.

Cubes can be programmed to perform simple LED light animations autonomously using the `LightState` structure and the
`CubeId.rotation_period_frames` field.

See `examples/cube_lights.py` and `examples/cube_light_animation.py` for example usage.


Cube Battery Voltage
--------------------

Cube battery voltage is communicated periodically with `ObjectPowerLevel` messages.


Cube Accelerometers
-------------------

Cube accelerometer value reception can be enabled with the `StreamObjectAccel` message and are communicated every 30 ms
with the `ObjectAccel` message.

In addition, the robot performs basic cube accelerometer ata processing and provides basic events with the following
messages:  

- `ObjectMoved`
- `ObjectStoppedMoving`
- `ObjectUpAxisChnaged`
- `ObjectTapped`
- `ObjectTapFiltered`


Animations
----------

To play animations, `AnimationState` message have to be enabled first using the `EnableAnimationState` message.

Animations are controlled with the `StartAnimation`, `EndAnimation`, and `AbortAnimation` messages.

Keyframes are transferred with the `AnimHead`, `AnimLift`, `AnimBody`, `AnimBackpackLights`, `RecordHeading`,
`TurnToRecordedHeading`, and `OutputAudio` messages.
   
See `examples/anim.py` for example usage.
