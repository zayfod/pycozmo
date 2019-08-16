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

    colors = [
        pycozmo.lights.red,
        pycozmo.lights.green,
        pycozmo.lights.blue,
        pycozmo.lights.white,
        pycozmo.lights.off,
    ]
    for color in colors:
        pkt = pycozmo.protocol_encoder.LightStateCenter(
            on_color_top=color.to_int16(),
            off_color_top=color.to_int16(),
            on_color_middle=color.to_int16(),
            off_color_middle=color.to_int16(),
            on_color_bottom=color.to_int16(),
            off_color_bottom=color.to_int16())
        cli.send(pkt)

        pkt = pycozmo.protocol_encoder.LightStateSide(
            on_color_left=color.to_int16(),
            off_color_left=color.to_int16(),
            on_color_right=color.to_int16(),
            off_color_right=color.to_int16())
        cli.send(pkt)
        time.sleep(2)

    cli.send_disconnect()
    time.sleep(1)


if __name__ == '__main__':
    main()
