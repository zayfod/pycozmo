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

    lights = [
        pycozmo.lights.red_light,
        pycozmo.lights.green_light,
        pycozmo.lights.blue_light,
        pycozmo.lights.off_light,
    ]
    for light in lights:
        # Select cube
        pkt = pycozmo.protocol_encoder.CubeId(object_id=cube_id)
        cli.conn.send(pkt)
        # Set lights
        pkt = pycozmo.protocol_encoder.CubeLights(states=(light, light, light, light))
        cli.conn.send(pkt)

        time.sleep(2)
