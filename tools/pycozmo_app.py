#!/usr/bin/env python
"""

PyCozmo application.

"""

import sys
import time
import argparse

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):
    brain = pycozmo.brain.Brain(cli)
    brain.start()
    while True:
        try:
            time.sleep(1.0)
        except KeyboardInterrupt:
            break
    brain.stop()


def parse_args():
    """ Parse command-line arguments. """
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    return args


def main():
    # Parse command-line.
    args = parse_args()     # noqa

    try:
        pycozmo.run_program(
            pycozmo_program,
            protocol_log_level="INFO",
            robot_log_level="INFO")
    except Exception as e:
        print("ERROR: {}".format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
