#!/usr/bin/env python

import time

import pycozmo


def on_robot_state(cli, pkt):
    del cli
    print("Battery level: {:.01f} V".format(pkt.battery_voltage))


def on_robot_poked(cli, pkt):
    del cli, pkt
    print("Poked!")


def pycozmo_program(cli):

    cli.add_handler(pycozmo.protocol_encoder.RobotState, on_robot_state, one_shot=True)
    cli.add_handler(pycozmo.protocol_encoder.RobotPoked, on_robot_poked)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


pycozmo.run_program(pycozmo_program)
