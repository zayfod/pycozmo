Revision History
================

v0.4.0 (Sep 13, 2019)
---------------------
- New commands: Enable, TurnInPlace, DriveStraight, ButtonPressed, HardwareInfo, BodyInfo, EnableColorImages,
    EnableStopOnCliff, NvStorageOp, NvStorageOpResult, FirmwareUpdate, FirmwareUpdateResult.
- New events: AnimationState, ObjectAvailable, ImageIMUData.
- New examples: cube_lights.py, charger_lights.py, cube_light_animation.py.
- Improved handling of 0x04 frames
- Added support for Int8, Int32, and enumeration packet fields.
- Improved robot state access.
- Added object availability and animation state access.
- Added initial pycozmo_replay.py tool for replaying .pcap files to Cozmo.
- Added OLED display initial image encoder code. 
- Added initial function description.

v0.3.0 (Sep 1, 2019)
--------------------
- Camera control and image reconstruction commands.
- Initial robot state commands (coordinates, orientation, track speed, battery voltage).
- Cube control commands.
- Fall detection commands.
- Audio volume control command.
- Firmware signature identification commands.
- Improved logging control.
- Python 3.5 compatibility fixes (thanks to Cyke).

v0.2.0 (Aug 25, 2019)
---------------------
- Backpack light control commands and example.
- Raw display control commands and example.
- Audio output commands and example.

v0.1.0 (Aug 15, 2019)
---------------------
- Initial release.
