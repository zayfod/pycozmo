#!/usr/bin/env python

import time

import pycozmo


def on_robot_state(conn: pycozmo.conn.Connection, pkt: pycozmo.protocol_encoder.RobotState) -> None:
    print("Battery level: {:.01f} V".format(pkt.battery_voltage))


def on_robot_poked(conn: pycozmo.conn.Connection, pkt: pycozmo.protocol_encoder.RobotPoked) -> None:
    print("Robot poked.")


def on_robot_falling_started(conn: pycozmo.conn.Connection, pkt: pycozmo.protocol_encoder.FallingStarted) -> None:
    print("Started falling.")


def on_robot_falling_stopped(conn: pycozmo.conn.Connection, pkt: pycozmo.protocol_encoder.FallingStopped) -> None:
    print("Falling stopped after {} ms. Impact intensity {:.01f}.".format(pkt.duration_ms, pkt.impact_intensity))


def on_button_pressed(conn: pycozmo.conn.Connection, pkt: pycozmo.protocol_encoder.ButtonPressed) -> None:
    if pkt.pressed:
        print("Button pressed.")
    else:
        print("Button released.")


def on_robot_picked_up(cli: pycozmo.Client, state: bool) -> None:
    if state:
        print("Picked up.")
    else:
        print("Put down.")


def on_robot_charging(cli: pycozmo.Client, state: bool) -> None:
    if state:
        print("Started charging.")
    else:
        print("Stopped charging.")


def on_cliff_detected(cli: pycozmo.Client, state: bool) -> None:
    if state:
        print("Cliff detected.")


def on_robot_wheels_moving(cli: pycozmo.Client, state: bool) -> None:
    if state:
        print("Started moving.")
    else:
        print("Stopped moving.")


def on_robot_orientation_change(cli: pycozmo.Client, orientation: pycozmo.robot.RobotOrientation) -> None:
    if orientation == pycozmo.robot.RobotOrientation.ON_THREADS:
        print("On threads.")
    elif orientation == pycozmo.robot.RobotOrientation.ON_BACK:
        print("On back.")
    elif orientation == pycozmo.robot.RobotOrientation.ON_FACE:
        print("On front.")
    elif orientation == pycozmo.robot.RobotOrientation.ON_LEFT_SIDE:
        print("On left side.")
    elif orientation == pycozmo.robot.RobotOrientation.ON_RIGHT_SIDE:
        print("On right side.")


# Change the robot log level to DEBUG to see robot debug messages related to events.
with pycozmo.connect(enable_animations=False, robot_log_level="INFO") as cli:

    cli.add_handler(pycozmo.protocol_encoder.RobotState, on_robot_state, one_shot=True)
    cli.add_handler(pycozmo.protocol_encoder.RobotPoked, on_robot_poked)
    cli.add_handler(pycozmo.protocol_encoder.FallingStarted, on_robot_falling_started)
    cli.add_handler(pycozmo.protocol_encoder.FallingStopped, on_robot_falling_stopped)
    cli.add_handler(pycozmo.protocol_encoder.ButtonPressed, on_button_pressed)
    cli.add_handler(pycozmo.event.EvtRobotPickedUpChange, on_robot_picked_up)
    cli.add_handler(pycozmo.event.EvtRobotChargingChange, on_robot_charging)
    cli.add_handler(pycozmo.event.EvtCliffDetectedChange, on_cliff_detected)
    cli.add_handler(pycozmo.event.EvtRobotWheelsMovingChange, on_robot_wheels_moving)
    cli.add_handler(pycozmo.event.EvtRobotOrientationChange, on_robot_orientation_change)

    while True:
        time.sleep(0.1)
