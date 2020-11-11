#!/usr/bin/env python

import time

import pycozmo


def on_robot_state(cli, pkt: pycozmo.protocol_encoder.RobotState):
    if pkt.pose_angle_rad < -0.4:
        state = "LS"
    elif pkt.pose_angle_rad > 0.4:
        state = "RS"
    elif pkt.pose_pitch_rad < -1.0:
        state = "F"
    elif pkt.pose_pitch_rad > 1.0:
        state = "B"
    else:
        state = "-"
    print("{:6.02f}\t{:6.03f}\t{}".format(
          pkt.pose_angle_rad, pkt.pose_pitch_rad, state))


with pycozmo.connect(enable_animations=False) as cli:

    cli.add_handler(pycozmo.protocol_encoder.RobotState, on_robot_state)

    while True:
        time.sleep(0.1)
