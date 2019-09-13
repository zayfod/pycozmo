Cozmo Functions
===============


Overview
--------

### Head

`HardwareInfo`
`FirmwareSignature`

### Body

`BodyInfo`

### Cubes

- LEDs
- Accelerometers
- Battery voltage

### Charging Platform

Some charging platforms (aka "pads") can be communicated with over Bluetooth LE. They contains 3 RGB LEDs that can be
controlled, similar to cube LEDs.


Wi-Fi
-----

Wi-Fi is activated automatically when the head board is powered on. The robot operates in access point mode.

`cozmoclad` defines a `SetBodyRadioMode` message that seems to allow changing the Wi-Fi channel but it is unclear
how it can be used with the Cozmo protocol.


Backpack LEDs
-------------

The 5 Backpack LEDs can be set controlled with 2 messages:
- `lightStateCenter` - controls the top, middle, and bottom RGB LEDs.
- `LightStateSide` - controls the left and right red-only LEDs.

Each color is defined by a 5-bit value for a total of 32768 colors.

See [backpack_lights.py](../examples/backpack_lights.py) for example usage.


Backpack Button
---------------

Newer Cozmo models have a backpack button. The `RobotState` message has a `backpack_touch_sensor_raw` field but
it seems that it's value does not change as a result of button presses. 

Button press and release events are communicated bu the `ButtonPressed` message. It is immediately available on
connection and does not require `Enable` to be used.


Wheels
------

The left and the right motor speeds can be controlled directly using the `DriveWheels` and `TurnInPlaceAtSpeed`
messages.

In addition, the motors can be stopped using the `StopAllMotors` message.

The actual speed of wheels is measured with Hall magnetic sensors. The values for each wheel can be
read through the `lwheel_speed_mmps` and `rwheel_speed_mmps` fields of the `RobotState` message.

`TurnInPlace`
`DriveStraight`


Localization
------------

`RobotState`
`RobotDelocalized`


Head
----

The head motor can be controlled directly, using the `DriveHead` and `SetHeadAngle` messages.

In addition, the motor can be stopped using the `StopAllMotors` message.

The actual head angle can be read through the `head_angle_rad` field of the `RobotState` message.

See [extremes.py](../examples/extremes.py) for example usage.

`AcknowledgeAction`


Lift
----

The head motor can be controlled directly, using the `DriveLift` and `SetLiftHeight` messages.

In addition, the motor can be stopped using the `StopAllMotors` message.

The actual lift height can be read through the `lift_height_mm` field of the `RobotState` message.

See [extremes.py](../examples/extremes.py) for example usage.

`AcknowledgeAction`


OLED display
------------

See [display.py](../examples/display.py) for example usage.

`NextFrame`
`DisplayImage`
`AnimationState`


Speaker
-------

See [audio.py](../examples/audio.py) for example usage. 

`OutputAudio`
`SetRobotVolume`
`AnimationState`


Camera
------

See [camera.py](../examples/camera.py) for example usage. 

`EnableCamera`
`SetCameraParams`
`EnableColorImages`
`ImageChunk`
`ImageImuData`


IR LED
------

The IR head light can be turned on and off using the `SetHeadLight` message.


Accelerometers
--------------

See [events.py](../examples/events.py) for example usage.

`RobotState`
`RobotPoked`
`FallingStarted`
`FallingStopped`


Gyro
----

`RobotState`


Cliff Sensor
------------

`RobotState`
`EnableStopOnCliff`


Battery voltage
---------------

`RobotState`


NV RAM Storage
--------------

`NvStorageOp`
`NvStorageOpResult`


Firmware Updates
----------------

Cozmo firmware updates are distributed in "cozmo.safe" files that seem to contain firmware images for all three of
Cozmos controllers - the Wi-Fi controller (Espressif ESP8266), the body controller (NXP Kinetis K02), and the Bluetooth
LE controller (Nordic nRF51822).

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

See [versions.md](versions.md) for more examples.

There seem to be individual signatures for each controller but the structure of the `cozmo.safe` files is not known.

The firmware image is transferred as-is from the engine to the robot, using `FirmwareUpdate` messages. It is divided
into 1024 B chunks that are numbered consecutively, starting with 0. Each chunk is confirmed by the robot with a
`FirmwareUpdateResult` message with `status` field set to 0.

Firmware transfer completion is indicated by the engine with e `FirmwareUpdate` message with chunk ID set to 0xFFFF and
data set to all-zeros. The robot confirms firmware update completion by sending a `FirmwareUpdateResult` message that
repeats the last chunk ID and has a `status` field set to 10.


Bluetooth LE
------------

"Objects", that can be connected to over Bluettoth LE announce their availability with an `ObjectAvailable` message
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


Cube Battery Voltage
--------------------

`ObjectPowerLevel`


Cube Accelerometers
-------------------

`ObjectMoved`
`ObjectStoppedMoving`
`ObjectUpAxisChnaged`
`ObjectTapped`
`ObjectTapFiltered`
