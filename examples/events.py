#!/usr/bin/env python

import time

import pycozmo


def on_robot_state(cli, pkt: pycozmo.protocol_encoder.RobotState):
    del cli
    print("Battery level: {:.01f} V".format(pkt.battery_voltage))


def on_robot_poked(cli, pkt: pycozmo.protocol_encoder.RobotPoked):
    del cli, pkt
    print("Robot poked.")


def on_robot_falling_started(cli, pkt: pycozmo.protocol_encoder.FallingStarted):
    del cli, pkt
    print("Started falling.")


def on_robot_falling_stopped(cli, pkt: pycozmo.protocol_encoder.FallingStopped):
    del cli
    print("Falling stopped after {} ms. Impact intensity {:.01f}.".format(pkt.duration_ms, pkt.impact_intensity))


def on_robot_picked_up(cli, state):
    del cli
    if state:
        print("Picked up.")
    else:
        print("Put down.")


def on_robot_charging(cli, state):
    del cli
    if state:
        print("Started charging.")
    else:
        print("Stopped charging.")


def on_cliff_detected(cli, state):
    del cli
    if state:
        print("Cliff detected.")


def on_robot_wheels_moving(cli, state):
    del cli
    if state:
        print("Started moving.")
    else:
        print("Stopped moving.")


def pycozmo_program(cli: pycozmo.client.Client):

    cli.add_handler(pycozmo.protocol_encoder.RobotState, on_robot_state, one_shot=True)
    cli.add_handler(pycozmo.protocol_encoder.RobotPoked, on_robot_poked)
    cli.add_handler(pycozmo.protocol_encoder.FallingStarted, on_robot_falling_started)
    cli.add_handler(pycozmo.protocol_encoder.FallingStopped, on_robot_falling_stopped)
    cli.add_handler(pycozmo.client.EvtRobotPickedUpChange, on_robot_picked_up)
    cli.add_handler(pycozmo.client.EvtRobotChargingChange, on_robot_charging)
    cli.add_handler(pycozmo.client.EvtCliffDetectedChange, on_cliff_detected)
    cli.add_handler(pycozmo.client.EvtRobotWheelsMovingChange, on_robot_wheels_moving)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


pycozmo.run_program(pycozmo_program)
