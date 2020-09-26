"""

Helper functions for running PyCozmo applications.

"""

from typing import Optional, Callable
import sys
import os
import logging

from . import logger, logger_protocol, logger_robot
from . import client
from . import exception


__all__ = [
    'setup_basic_logging',
    'run_program',
]


def setup_basic_logging(
        log_level: Optional[str] = None,
        protocol_log_level: Optional[str] = None,
        robot_log_level: Optional[str] = None,
        target=sys.stderr) -> None:

    if log_level is None:
        log_level = os.environ.get('PYCOZMO_LOG_LEVEL', logging.INFO)
    if protocol_log_level is None:
        protocol_log_level = os.environ.get('PYCOZMO_PROTOCOL_LOG_LEVEL', logging.INFO)
    if robot_log_level is None:
        # Keeping the default to WARNING due to "AnimationController.IsReadyToPlay.BufferStarved" messages.
        robot_log_level = os.environ.get('PYCOZMO_ROBOT_LOG_LEVEL', logging.WARNING)
    handler = logging.StreamHandler(stream=target)
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(name)-20s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    logger_protocol.addHandler(handler)
    logger_protocol.setLevel(protocol_log_level)
    logger_robot.addHandler(handler)
    logger_robot.setLevel(robot_log_level)


def run_program(
        f: Callable,
        log_level: Optional[str] = None,
        protocol_log_level: Optional[str] = None,
        protocol_log_messages: Optional[list] = None,
        robot_log_level: Optional[str] = None,
        auto_initialize: bool = True) -> None:

    setup_basic_logging(log_level=log_level, protocol_log_level=protocol_log_level, robot_log_level=robot_log_level)

    try:
        cli = client.Client(protocol_log_messages=protocol_log_messages, auto_initialize=auto_initialize)
        cli.start()
        cli.connect()
        cli.wait_for_robot()
    except exception.PyCozmoException as e:
        logger.error(e)
        sys.exit(1)

    try:
        # Exceptions, generated from the application are intentionally not handled.
        f(cli)
    except KeyboardInterrupt:
        logger.info("Interrupted...")
    finally:
        cli.disconnect()
        cli.stop()

    logger.info("Done.")
