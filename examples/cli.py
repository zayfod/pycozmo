#!/usr/bin/env python

import time

from pycozmo.client import Client


def run():
    cli = Client()
    cli.start()
    cli.connect()

    while cli.state != Client.CONNECTED:
        time.sleep(0.2)

    while True:
        cmd = input()
        if cmd == "q":
            break
        elif cmd == "e":
            cli.send_enable()
        elif cmd == "o":
            cli.send_led()

    cli.send_disconnect()


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterrupted...")


if __name__ == '__main__':
    main()
