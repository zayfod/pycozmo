#!/usr/bin/env python

from threading import Event

import pycozmo


SPEED_MMPS = 100.0
ACCEL_MMPS2 = 20.0
DECEL_MMPS2 = 20.0

e = Event()


def on_path_following_event(cli, pkt: pycozmo.protocol_encoder.PathFollowingEvent):
    print(pkt.event_type)
    if pkt.event_type != pycozmo.protocol_encoder.PathEventType.PATH_STARTED:
        e.set()


def on_robot_pathing_change(cli, state: bool):
    if state:
        print("Started pathing.")
    else:
        print("Stopped pathing.")


with pycozmo.connect() as cli:

    cli.add_handler(pycozmo.protocol_encoder.PathFollowingEvent, on_path_following_event)
    cli.add_handler(pycozmo.event.EvtRobotPathingChange, on_robot_pathing_change)

    pkt = pycozmo.protocol_encoder.AppendPathSegLine(
        from_x=0.0, from_y=0.0,
        to_x=150.0, to_y=0.0,
        speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
    cli.conn.send(pkt)
    pkt = pycozmo.protocol_encoder.AppendPathSegLine(
        from_x=150.0, from_y=0.0,
        to_x=150.0, to_y=150.0,
        speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
    cli.conn.send(pkt)
    pkt = pycozmo.protocol_encoder.AppendPathSegLine(
        from_x=150.0, from_y=150.0,
        to_x=0.0, to_y=150.0,
        speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
    cli.conn.send(pkt)
    pkt = pycozmo.protocol_encoder.AppendPathSegLine(
        from_x=0.0, from_y=150.0,
        to_x=0.0, to_y=0.0,
        speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
    cli.conn.send(pkt)
    pkt = pycozmo.protocol_encoder.AppendPathSegPointTurn(
        x=0.0, y=0.0,
        angle_rad=pycozmo.util.Angle(degrees=0.0).radians,
        angle_tolerance_rad=0.01,
        speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
    cli.conn.send(pkt)

    pkt = pycozmo.protocol_encoder.ExecutePath(event_id=1)
    cli.conn.send(pkt)

    e.wait(timeout=30.0)
