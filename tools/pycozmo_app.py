#!/usr/bin/env python
"""

PyCozmo application.

"""

import sys
import time
import argparse

import pycozmo


def parse_args():
    """ Parse command-line arguments. """
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    return args


def brain(cli: pycozmo.client.Client):
    """ Perform robot OTA firmware update. """
    brain = pycozmo.brain.Brain(cli)
    brain.start()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
    brain.stop()


def main():
    # Parse command-line.
    args = parse_args()     # noqa

    # Update robot.
    try:
        pycozmo.run_program(
            brain,
            protocol_log_level="INFO",
            robot_log_level="DEBUG",
            auto_initialize=False)
    except Exception as e:
        print("ERROR: {}".format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
