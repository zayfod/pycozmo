"""

Helper functions for running PyCozmo applications.

"""

from typing import Optional
import sys
import os
import logging

from . import logger, logger_protocol
from . import client


__all__ = [
    'setup_basic_logging',
    'run_program',
]


def setup_basic_logging(log_level: Optional[str] = None, protocol_log_level: Optional[str] = None,
                        target=sys.stderr) -> None:
    if log_level is None:
        log_level = os.environ.get('PYCOZMO_LOG_LEVEL', logging.INFO)
    if protocol_log_level is None:
        protocol_log_level = os.environ.get('PYCOZMO_PROTOCOL_LOG_LEVEL', logging.WARNING)
    handler = logging.StreamHandler(stream=target)
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(name)-20s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    logger_protocol.addHandler(handler)
    logger_protocol.setLevel(protocol_log_level)


def run_program(f: callable, log_level: Optional[str] = None, protocol_log_level: Optional[str] = None,
                protocol_log_messages: Optional[list] = None) -> None:
    setup_basic_logging(log_level=log_level, protocol_log_level=protocol_log_level)

    cli = client.Client(protocol_log_messages=protocol_log_messages)
    cli.start()
    cli.connect()
    cli.wait_for_robot()

    try:
        f(cli)
    except KeyboardInterrupt:
        logger.info("Interrupted...")
    finally:
        cli.disconnect()
        cli.stop()

    logger.info("Done.")
