#!/usr/bin/env python

import time

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):

    # Load animations - one time.
    cli.load_anims(str(pycozmo.util.get_cozmo_anim_dir()))

    # Print the names of all available animations.
    names = cli.get_anim_names()
    for name in sorted(names):
        print(name)

    time.sleep(2)

    # Play an animation.
    cli.play_anim("anim_launch_wakeup_01")


pycozmo.run_program(pycozmo_program)
