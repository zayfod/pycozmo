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
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    args = parser.parse_args()
    return args


def main():
    # Parse command-line.
    args = parse_args()     # noqa

    try:
        with pycozmo.connect(
                log_level="DEBUG" if args.verbose else "INFO",
                protocol_log_level="INFO",
                robot_log_level="INFO") as cli:
            brain = pycozmo.brain.Brain(cli)
            brain.start()
            while True:
                try:
                    time.sleep(1.0)
                except KeyboardInterrupt:
                    break
            brain.stop()
    except Exception as e:
        print("ERROR: {}".format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
