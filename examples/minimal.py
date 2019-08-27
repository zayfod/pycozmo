#!/usr/bin/env python

import time

import pycozmo


def main():
    cli = pycozmo.Client()
    cli.start()
    cli.connect()

    while cli.state != pycozmo.Client.CONNECTED:
        time.sleep(0.2)

    cli.send_enable()
    time.sleep(1)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    cli.send_disconnect()
    time.sleep(1)


if __name__ == '__main__':
    main()
