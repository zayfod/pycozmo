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

    lights = [
        pycozmo.lights.red_light,
        pycozmo.lights.green_light,
        pycozmo.lights.blue_light,
        pycozmo.lights.white_light,
        pycozmo.lights.off_light,
    ]
    for light in lights:
        pkt = pycozmo.protocol_encoder.LightStateCenter(states=(light, light, light))
        cli.send(pkt)

        pkt = pycozmo.protocol_encoder.LightStateSide(states=(light, light))
        cli.send(pkt)

        time.sleep(2)

    cli.send_disconnect()
    time.sleep(1)


if __name__ == '__main__':
    main()
