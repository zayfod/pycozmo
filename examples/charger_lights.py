#!/usr/bin/env python

import time

import pycozmo


with pycozmo.connect() as cli:

    print("Waiting for charger...")
    charger_factory_id = None
    while not charger_factory_id:
        available_objects = dict(cli.available_objects)
        for factory_id, obj in available_objects.items():
            if obj.object_type == pycozmo.protocol_encoder.ObjectType.Charger_Basic:
                charger_factory_id = factory_id
                break
    print("Charger with S/N 0x{:08x} available.".format(charger_factory_id))

    print("Connecting to charger...")
    pkt = pycozmo.protocol_encoder.ObjectConnect(factory_id=charger_factory_id, connect=True)
    cli.conn.send(pkt)
    cli.conn.wait_for(pycozmo.protocol_encoder.ObjectConnectionState)
    charger_id = list(cli.connected_objects.keys())[0]
    print("Charger connected - ID {}.".format(charger_id))

    lights = [
        pycozmo.lights.red_light,
        pycozmo.lights.green_light,
        pycozmo.lights.blue_light,
        pycozmo.lights.off_light,
    ]
    for light in lights:
        # Select
        pkt = pycozmo.protocol_encoder.CubeId(object_id=charger_id)
        cli.conn.send(pkt)
        # Set lights
        pkt = pycozmo.protocol_encoder.CubeLights(states=(light, light, light, pycozmo.lights.off_light))
        cli.conn.send(pkt)

        time.sleep(2)
