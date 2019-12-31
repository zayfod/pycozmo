
Overview
========

`PyCozmo` is a pure-Python [Anki Cozmo](https://anki.com/en-us/cozmo.html) communication library. It allows controlling
a Cozmo robot directly, without having to go through a mobile device, running the Cozmo app.

The library is loosely based on the [Anki Cozmo Python SDK](https://github.com/anki/cozmo-python-sdk) and the
[cozmoclad](https://pypi.org/project/cozmoclad/) ("C-Like Abstract Data") library.

This project is a tool for exploring the hardware and software of Anki Cozmo. It is unstable and heavily under
development.


Usage
-----

Basic mode:
```python
import time
import pycozmo

def pycozmo_program(cli):
    cli.set_head_angle(angle=0.6)
    time.sleep(1)

pycozmo.run_program(pycozmo_program)
```

Advanced mode:
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
+------------------+                     +------------------+                     +------------------+
|     SDK app      |      Cozmo SDK      |    Cozmo app     |       PyCozmo       |      Cozmo       |
|      "game"      |      cozmoclad      |     "engine"     |                     |     "robot"      |
|                  | ------------------> |   Wi-Fi client   | ------------------> |     Wi-Fi AP     |
|                  |         USB         |    UDP client    |      UDP/Wi-Fi      |    UDP Server    |
+------------------+                     +------------------+                     +------------------+
```


Requirements
------------

- Python 3.5.4
- [Pillow](https://github.com/python-pillow/Pillow) 6.0.0 - Python image library
- [FlatBuffers](https://github.com/google/flatbuffers) - serialization library
- [dpkt](https://github.com/kbandla/dpkt) - TCP/IP packet parsing library 


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

From source, for development:

```
git clone git@github.com:zayfod/pycozmo.git
cd pycozmo
python setup.py develop
```

 
Support
-------

Bug reports and patches should be sent via GitHub:

[https://github.com/zayfod/pycozmo](https://github.com/zayfod/pycozmo)

Anki Robot Discord server, channel #cozmo:

[https://discord.gg/ew92haS](https://discord.gg/ew92haS)


Disclaimer
----------

This project is not affiliated with [Anki](https://anki.com/) or
[Digital Dream Labs](https://www.digitaldreamlabs.com/).
