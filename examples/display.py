#!/usr/bin/env python

import time

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):

    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    pkt = pycozmo.protocol_encoder.SetHeadAngle(angle_rad=angle)
    cli.conn.send(pkt)

    for _ in range(3):
        pkt = pycozmo.protocol_encoder.NextFrame()
        cli.conn.send(pkt)
        pkt = pycozmo.protocol_encoder.DisplayImage(pycozmo.util.hex_load(
            "11:9c:b6:a4:98:be:40:94:c6:40:90:ce:5b:94:c6:9c:98:be:a0:"
            "9c:b6:06:a0:ae:40:9c:b6:40:98:be:5d:9c:b6:40:a0:ae:1b"))
        cli.conn.send(pkt)
        time.sleep(1)

        pkt = pycozmo.protocol_encoder.NextFrame()
        cli.conn.send(pkt)
        pkt = pycozmo.protocol_encoder.DisplayImage(pycozmo.util.hex_load(
            "16:a0:b6:41:9c:be:40:98:c6:5b:9c:be:9c:a0:b6:40:06:a4:ae:"
            "a4:a0:b6:40:9c:be:40:98:c6:5b:9c:be:40:a0:b6:40:16"))
        cli.conn.send(pkt)
        time.sleep(1)


pycozmo.run_program(pycozmo_program)
