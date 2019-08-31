
import logging


__all__ = [
    "logger",
    "logger_protocol",
]

logger = logging.getLogger("pycozmo.general")
logger_protocol = logging.getLogger("pycozmo.protocol")
