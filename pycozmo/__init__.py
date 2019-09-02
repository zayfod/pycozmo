
import sys

from .logging import *
from .run import *

from .frame import Frame
from .client import ROBOT_ADDR, Client, EvtRobotFound, EvtRobotReady
from .robot import *
from .event import *

from . import util
from . import protocol_base
from . import protocol_declaration
from . import protocol_generator
from . import protocol_encoder
from . import protocol_utils
from . import lights
from . import camera
from . import object


__version__ = "0.4.0"

__all__ = [
    "logger",
    "logger_protocol",

    "Frame",
    "ROBOT_ADDR",
    "Client",

    "MIN_HEAD_ANGLE_RAD",
    "MAX_HEAD_ANGLE_RAD",
    "MIN_LIFT_HEIGHT_MM",
    "MAX_LIFT_HEIGHT_MM",
    "LIFT_ARM_LENGTH_MM",
    "LIFT_PIVOT_HEIGHT_MM",
    "MAX_WHEEL_SPEED_MMPS",

    "setup_basic_logging",
    "run_program",
]

if sys.version_info < (3, 5):
    sys.exit("ERROR: PyCozmo requires Python 3.5 or newer.")
del sys
