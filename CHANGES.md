Revision History
================

v0.8.0 (Nov 12, 2020)
---------------------
- New animation controller that synchronizes animations, audio playback, and image displaying.
- Procedural face generation to bring the roboto to life.
- Loading of Cozmo resource files - activities, behaviors, emotions, light animations
    (thanks to Aitor Miguel Blanco / gimait)
- pycozmo.audiokinetic module for working with Audiokinetic WWise SoundBank files.
- New tool for managing Cozmo resources - pycozmo_resources.py .
- Initial Cozmo application with rudimentary reactions and behaviors - pycozmo_app.py .
- Cozmo protocol client robustness improvements.
- CLAD encoding optimizations.
- Cliff detection and procedural face rendering improvements (thanks to Aitor Miguel Blanco / gimait)
- Replaced pycozmo.run_program() with pycozmo.connect() context manager. 
- Renamed the NextFrame packet to OutputSilence to better describe its function.
- Dropped support for Python 3.5 and added support for Python 3.9.
- Bug fixes and documentation improvements.

v0.7.0 (Sep 26, 2020)
---------------------
- Full robot audio support and a new AudioManager class (thanks to Aitor Miguel Blanco / gimait).  
- Cozmo protocol client robustness improvements (thanks to Aitor Miguel Blanco / gimait):
    - frame retransmission
    - transmission of multiple packets in a single frame
- Procedural face rendering improvements (thanks to Catherine Chambers / ca2-chambers).
- Added support for robot firmware debug message decoding.
- Added a new video.py example.
- Added a tool for over-the-air firmware updates - pycozmo_update.py (thanks to Einfari).
- Added hardware version description.
- Bug fixes and documentation improvements.

v0.6.0 (Jan 2, 2020)
--------------------
- Improved localization - SetOrigin and SyncTime commands and pose (position and orientation) interpretation.
- Added new path tracking commands (AppendPath*, ExecutePath, etc.) and examples (path.py, go_to_pose.py). 
- Added support for drawing procedural faces (thanks to Pedro Tiago Pereira / ppedro74).
- Added support for reading and writing animations in FlatBuffers (.bin) and JSON format.
- Added a new tool for examining and manipulating animation files - pycozmo_anim.py .
- Added commands for working with cube/object accelerometers - StreamObjectAccel, ObjectAccel.
- Improved function description. 
- Bug fixes and documentation improvements.

v0.5.0 (Oct 12, 2019)
---------------------
- Added initial client API.
- Separated low-level Cozmo connection handling into a new ClientConnection class.
- Improved the ImageDecoder class and added a new ImageEncoder class for handling Cozmo protocol image encoding.
- Added new examples for displaying images from files and drawing on Cozmo's OLED display.
- New protocol commands: EnableBodyACC, EnableAnimationState, AnimHead, AnimLift, AnimBackpackLights, AnimBody,
    StartAnimation, EndAnimation, AnimationStarted, AnimationEnded, DebugData.
- Initial support for Cozmo animations in FlatBuffer .bin files.
- Improved filtering through packet groups for pycozmo_dump.py and pycozmo_replay.py .
- Added type hints in the protocol generator.
- Bug fixes and documentation improvements.

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
- Added initial pycozmo_replay.py tool for replaying PCAP files to Cozmo.
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
