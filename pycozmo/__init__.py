
import sys

from .logging import *
from .run import *

from .frame import Frame
from .client import ROBOT_ADDR, Client, EvtRobotFound, EvtRobotReady
from .robot import *
from .event import *

from . import exception
from . import util
from . import protocol_base
from . import protocol_declaration
from . import protocol_generator
from . import protocol_encoder
from . import protocol_utils
from . import lights
from . import camera
from . import object
from . import filter
from . import anim


__version__ = "0.5.0"

__all__ = [
    "logger",
    "logger_protocol",

    "Frame",
    "ROBOT_ADDR",
    "Client",

    "setup_basic_logging",
    "run_program",
]

if sys.version_info < (3, 5, 4):
    sys.exit("ERROR: PyCozmo requires Python 3.5.4 or newer.")
del sys
