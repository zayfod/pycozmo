#!/usr/bin/env python

import time

import pycozmo


def on_robot_state(cli, pkt: pycozmo.protocol_encoder.RobotState):
    del cli
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


def pycozmo_program(cli: pycozmo.client.Client):

    cli.add_handler(pycozmo.protocol_encoder.RobotState, on_robot_state)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


# Change the robot log level to DEBUG to see robot debug messages related to events.
pycozmo.run_program(pycozmo_program, enable_animations=False, robot_log_level="INFO")
