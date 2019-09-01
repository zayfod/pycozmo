PyCozmo
=======

`PyCozmo` is a pure-Python [Anki Cozmo](https://anki.com/en-us/cozmo.html) communication library. It allows controlling
a Cozmo robot directly, without having to go through a mobile device, running the Cozmo app.

The library is loosely based on the [Anki Cozmo Python SDK](https://github.com/anki/cozmo-python-sdk) and the
[cozmoclad](https://pypi.org/project/cozmoclad/) library.

This project is a tool for exploring the hardware and software of Anki Cozmo. It is unstable and heavily under
development.


Usage
-----

Basic mode:
```python
import time
import pycozmo

def pycozmo_program(cli):
    pkt = pycozmo.protocol_encoder.SetHeadAngle(angle_rad=0.6)
    cli.send(pkt)
    time.sleep(1)

pycozmo.run_program(pycozmo_program)
```

Advanced mode:
```python
import time
import pycozmo

cli = pycozmo.Client()
cli.start()
cli.connect()
cli.wait_for_robot()

pkt = pycozmo.protocol_encoder.DriveWheels(lwheel_speed_mmps=50.0, rwheel_speed_mmps=50.0) 
cli.send(pkt)
time.sleep(2.0)
pkt = pycozmo.protocol_encoder.StopAllMotors()
cli.send(pkt)

cli.disconnect()
cli.stop()
```


Documentation
-------------

- [Cozmo protocol](docs/protocol.md) description
- [Capturing Cozmo communication](docs/capturing.md)


Tools
-----

- `pycozmo_dump.py` - a command-line application that can read and annotate Cozmo communication from
    [pcap files](https://en.wikipedia.org/wiki/Pcap)


Examples
--------

- [rc.py](examples/rc.py) - turns Cozmo into an RC tank that can be driven with an XBox 360 Wireless Controller
- [extremes.py](examples/extremes.py) - demonstrates Cozmo lift and head control
- [backpack_lights.py](examples/backpack_lights.py) - demonstrates Cozmo backpack LED control
- [display.py](examples/display.py) - demonstrates low-level visualization of images on Cozmo's display
- [audio.py](examples/audio.py) - demonstrates 22 kHz, 8-bit, mono WAVE file playback through Cozmo's speaker 
- [events.py](examples/events.py) - demonstrates event handling
- [camera.py](examples/camera.py) - demonstrates capturing a camera image 


Robot Support
-------------

Sensors:
- Camera - supported
- Cliff sensor - not supported
- Accelerometers - work in progress
- Gyro - work in progress
- Battery voltage - supported
- Cube battery voltage - supported
- Cube accelerometers - supported

Actuators:
- Wheel motors - supported
- Head motor - supported
- Lift motor - supported
- Backpack LEDs - supported
- IR LED - supported
- OLED display - work in progress
- Speaker - supported
- Cube LEDs - supported

Communication:
- Wi-Fi AP - supported
- Bluetooth LE - supported


Connecting to Cozmo over Wi-Fi
------------------------------

A Wi-Fi connection needs to be established with Cozmo before using PyCozmo applications.

1. Wake up Cozmo by placing it on the charging platform
2. Make Cozmo display it's Wi-Fi PSK by rising and lowering its lift
3. Scan for Cozmo's Wi-Fi SSID (depends on the OS)
4. Connect using Cozmo's Wi-Fi PSK (depends on the OS)


PyCozmo vs. the Cozmo SDK
-------------------------

A Cozmo SDK application (aka "game") acts as a client to the Cozmo app (aka "engine") that runs on a mobile device.
The low-level communication happens over USB and is handled by the `cozmoclad` library.

In contrast, an application using PyCozmo basically replaces the Cozmo app and acts as the "engine". PyCozmo handles
the low-level UDP communication with Cozmo.
   
```
+------------------+                      +------------------+                      +------------------+
|     SDK app      |      Cozmo SDK       |    Cozmo app     |       PyCozmo        |      Cozmo       |
|      "game"      |      cozmoclad       |     "engine"     |                      |     "robot"      |
|                  | +------------------> |   Wi-Fi client   | +------------------> |     Wi-Fi AP     |
|                  |         USB          |    UDP client    |      UDP/Wi-Fi       |    UDP Server    |
+------------------+                      +------------------+                      +------------------+
```


Limitations
-----------

- some high-level Cozmo SDK features are implemented in the Cozmo app and have no equivalent in PyCozmo:
    - personality engine
    - behaviors
    - motion detection
    - text-to-speech
    - songs
- there is no Wi-Fi control. The library assumes a Wi-Fi connection to Cozmo, established in advance.
- frame retransmission is not implemented
- transmission of multiple packets in a single frame is not implemented


Requirements
------------

- Python 3.5


Installation
------------

Using pip:

```
pip install pycozmo
```

From source:

```
git clone https://github.com/zayfod/pycozmo.git
cd pycozmo
python setup.py install
```

 
Bugs
----

Bug reports and patches should be sent via GitHub:

https://github.com/zayfod/pycozmo
