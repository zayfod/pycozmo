#!/usr/bin/env python

import time

import pycozmo


def main():
    cli = pycozmo.Client()
    cli.start()
    cli.connect()
    cli.wait_for_robot()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    cli.disconnect()
    cli.stop()


if __name__ == '__main__':
    main()
