"""

Logging.

"""

import logging


__all__ = [
    "logger",
    "logger_protocol",
]


#: General logger.
logger = logging.getLogger("pycozmo.general")
#: Protocol logger.
logger_protocol = logging.getLogger("pycozmo.protocol")
