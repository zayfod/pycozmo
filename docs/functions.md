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
- BatteryVoltage

### Charging Platform


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

Newer Cozmo models have a backpack button. It seems that it's state can be accessed through the
`backpack_touch_sensor_raw` field of the `RobotState` message (unconfirmed).


Wheels
------

The left and the right motor speeds can be controlled directly using the `DriveWheels` and `TurnInPlace` messages.

In addition, the motors can be stopped using the `StopAllMotors` message.

The actual speed of wheels is measured with Hall magnetic sensors. The values for each wheel can be
read through the `lwheel_speed_mmps` and `rwheel_speed_mmps` fields of the `RobotState` message.


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

`AcknowledgeCommand`


Lift
----

The head motor can be controlled directly, using the `DriveLift` and `SetLiftHeight` messages.

In addition, the motor can be stopped using the `StopAllMotors` message.

The actual lift height can be read through the `lift_height_mm` field of the `RobotState` message.

See [extremes.py](../examples/extremes.py) for example usage.

`AcknowledgeCommand`


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


Bluetooth LE
------------

`ObjectAvailable`
`ObjectConnect`
`ObjectConnectionState`


Cube LEDs
---------

`CibeId`
`CubeLights`


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
