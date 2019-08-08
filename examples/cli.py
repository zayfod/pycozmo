#!/usr/bin/env python

import time

import pycozmo


def run():
    cli = pycozmo.Client()
    cli.start()
    cli.connect()

    while cli.state != pycozmo.Client.CONNECTED:
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
