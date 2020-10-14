"""

Logging.

"""

import logging


__all__ = [
    "logger",
    "logger_protocol",
    "logger_robot",
    "logger_reaction",
    "logger_behavior",
    "logger_animation",
]


# General logger - general PyCozmo log messages.
logger = logging.getLogger("pycozmo.general")
# Protocol logger - log messages related to the Cozmo protocol.
logger_protocol = logging.getLogger("pycozmo.protocol")
# Robot logger - log messages coming from the robot microcontrollers.
logger_robot = logging.getLogger("pycozmo.robot")
# Reaction logger.
logger_reaction = logging.getLogger("pycozmo.reaction")
# Behavior logger.
logger_behavior = logging.getLogger("pycozmo.behavior")
# Animation logger.
logger_animation = logging.getLogger("pycozmo.animation")
