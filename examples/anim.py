#!/usr/bin/env python

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):
    fspec = "com.anki.cozmo/files/cozmo/cozmo_resources/assets/animations/anim_codelab_tap.bin"
    clips = pycozmo.anim_encoder.AnimClips.from_fb_file(fspec)
    ppclip = pycozmo.anim.PreprocessedClip.from_anim_clip(clips.clips[0])
    cli.play_anim_clip(ppclip)


pycozmo.run_program(pycozmo_program)
