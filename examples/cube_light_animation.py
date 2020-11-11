#!/usr/bin/env python

import time

import pycozmo


with pycozmo.connect() as cli:

    print("Waiting for cube...")
    cube_factory_id = None
    while not cube_factory_id:
        available_objects = dict(cli.available_objects)
        for factory_id, obj in available_objects.items():
            if obj.object_type == pycozmo.protocol_encoder.ObjectType.Block_LIGHTCUBE1:
                cube_factory_id = factory_id
                break
    print("Cube with S/N 0x{:08x} available.".format(cube_factory_id))

    print("Connecting to cube...")
    pkt = pycozmo.protocol_encoder.ObjectConnect(factory_id=cube_factory_id, connect=True)
    cli.conn.send(pkt)
    cli.conn.wait_for(pycozmo.protocol_encoder.ObjectConnectionState)
    cube_id = list(cli.connected_objects.keys())[0]
    print("Cube connected - ID {}.".format(cube_id))

    color = pycozmo.lights.Color(int_color=0x00ff00ff)
    light = pycozmo.protocol_encoder.LightState(
        on_color=color.to_int16(),
        off_color=pycozmo.lights.off.to_int16(),
        on_frames=5,
        off_frames=20,
        transition_on_frames=5,
        transition_off_frames=10)

    # Select cube
    pkt = pycozmo.protocol_encoder.CubeId(object_id=cube_id, rotation_period_frames=40)
    cli.conn.send(pkt)
    # Set lights
    pkt = pycozmo.protocol_encoder.CubeLights(states=(
        light,
        pycozmo.lights.off_light,
        pycozmo.lights.off_light,
        pycozmo.lights.off_light))
    cli.conn.send(pkt)

    time.sleep(30.0)
