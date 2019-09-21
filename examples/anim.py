#!/usr/bin/env python

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):
    fspec = "com.anki.cozmo/files/cozmo/cozmo_resources/assets/animations/anim_codelab_tap.bin"
    clips = pycozmo.anim.load_anim_clips(fspec)
    clip = clips[0]
    cli.play_anim(clip)


pycozmo.run_program(pycozmo_program)
