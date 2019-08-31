#!/usr/bin/env python

import time

import pycozmo


def main():
    cli = pycozmo.Client()
    cli.start()
    cli.connect()
    cli.wait_for_robot()

    cli.send(pycozmo.protocol_encoder.SetHeadAngle(angle_rad=pycozmo.MAX_HEAD_ANGLE_RAD))
    time.sleep(1)
    cli.send(pycozmo.protocol_encoder.SetHeadAngle(angle_rad=pycozmo.MIN_HEAD_ANGLE_RAD))
    time.sleep(1)
    cli.send(pycozmo.protocol_encoder.DriveHead())

    cli.send(pycozmo.protocol_encoder.SetLiftHeight(height_mm=pycozmo.MAX_LIFT_HEIGHT_MM))
    time.sleep(1)
    cli.send(pycozmo.protocol_encoder.SetLiftHeight(height_mm=pycozmo.MIN_LIFT_HEIGHT_MM))
    time.sleep(1)
    cli.send(pycozmo.protocol_encoder.DriveLift())

    cli.disconnect()
    cli.stop()


if __name__ == '__main__':
    main()
