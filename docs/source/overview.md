
Overview
========

[https://github.com/zayfod/pycozmo](https://github.com/zayfod/pycozmo)

`PyCozmo` is a pure-Python communication library, alternative SDK, and application for the
[Cozmo robot](https://www.digitaldreamlabs.com/pages/cozmo) . It allows controlling a Cozmo robot directly, without
having to go through a mobile device, running the Cozmo app.

The library is loosely based on the [Anki Cozmo Python SDK](https://github.com/anki/cozmo-python-sdk) and the
[cozmoclad](https://pypi.org/project/cozmoclad/) ("C-Like Abstract Data") library.

This project is a tool for exploring the hardware and software of the Digital Dream Labs (originally Anki) Cozmo robot.
It is unstable and heavily under development.


Usage
-----

Basic:

```python
import time
import pycozmo

with pycozmo.connect() as cli:
    cli.set_head_angle(angle=0.6)
    time.sleep(1)
```

Advanced:

```python
import pycozmo

cli = pycozmo.Client()
cli.start()
cli.connect()
cli.wait_for_robot()

cli.drive_wheels(lwheel_speed=50.0, rwheel_speed=50.0, duration=2.0)

cli.disconnect()
cli.stop()
```


PyCozmo vs. the Cozmo SDK
-------------------------

A Cozmo SDK application (aka "game") acts as a client to the Cozmo app (aka "engine") that runs on a mobile device.
The low-level communication happens over USB and is handled by the `cozmoclad` library.

In contrast, an application using PyCozmo basically replaces the Cozmo app and acts as the "engine". PyCozmo handles
the low-level UDP communication with Cozmo.
   
```
+------------------+                   +------------------+                   +------------------+
|     SDK app      |     Cozmo SDK     |    Cozmo app     |       Cozmo       |      Cozmo       |
|      "game"      |     cozmoclad     |     "engine"     |      protocol     |     "robot"      |
|                  | ----------------> |   Wi-Fi client   | ----------------> |     Wi-Fi AP     |
|                  |        USB        |    UDP client    |     UDP/Wi-Fi     |    UDP Server    |
+------------------+                   +------------------+                   +------------------+
```


Requirements
------------

- [Python](https://www.python.org/downloads/) 3.11 or newer
- [Pillow](https://github.com/python-pillow/Pillow) 9.1 or newer - Python image library
- [FlatBuffers](https://github.com/google/flatbuffers) 2.0 or newer - serialization library
- [dpkt](https://github.com/kbandla/dpkt) - TCP/IP packet parsing library 
- [OpenCV](https://opencv.org/) 4.0.0 or newer - computer vision library


Installation
------------

Using pip:

```
pip install pycozmo

pycozmo_resources.py download
```

From source:

```
git clone https://github.com/zayfod/pycozmo.git
cd pycozmo
pip install .

pycozmo_resources.py download
```

From source, for development (requires pip 25.1 or newer):

```
git clone git@github.com:zayfod/pycozmo.git
cd pycozmo
pip install -e . --group dev

pycozmo_resources.py download
```

Running the tests and linters:

```
flake8
mypy
pytest
```

 
Support
-------

Bug reports and changes should be sent via GitHub:

[https://github.com/zayfod/pycozmo](https://github.com/zayfod/pycozmo)

Vector & Friends Discord server, channel #development-cozmo:

[https://discord.com/servers/vector-and-friends-527874754342944770](https://discord.com/servers/vector-and-friends-527874754342944770)


Disclaimer
----------

This project is not affiliated with [Digital Dream Labs](https://www.digitaldreamlabs.com/) or
[Anki](https://anki.com/).
