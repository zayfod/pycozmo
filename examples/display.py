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

    cli.send_init_display()

    for _ in range(30):
        pkt = pycozmo.protocol_encoder.NextFrame()
        cli.send(pkt)
        pkt = pycozmo.protocol_encoder.DisplayImage(pycozmo.util.hex_load("11:9c:b6:a4:98:be:40:94:c6:40:90:ce:5b:94:c6:9c:98:be:a0:9c:b6:06:a0:ae:40:9c:b6:40:98:be:5d:9c:b6:40:a0:ae:1b"))
        cli.send(pkt)
        time.sleep(1)

        pkt = pycozmo.protocol_encoder.NextFrame()
        cli.send(pkt)
        pkt = pycozmo.protocol_encoder.DisplayImage(pycozmo.util.hex_load("16:a0:b6:41:9c:be:40:98:c6:5b:9c:be:9c:a0:b6:40:06:a4:ae:a4:a0:b6:40:9c:be:40:98:c6:5b:9c:be:40:a0:b6:40:16"))
        cli.send(pkt)
        time.sleep(1)

    cli.send_disconnect()
    time.sleep(1)


if __name__ == '__main__':
    main()
