#!/usr/bin/env python

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):

    target = pycozmo.util.Pose(200, 100.0, 0.0, angle_z=pycozmo.util.Angle(degrees=0.0))
    cli.go_to_pose(target, relative_to_robot=True)


pycozmo.run_program(pycozmo_program, log_level="DEBUG")
