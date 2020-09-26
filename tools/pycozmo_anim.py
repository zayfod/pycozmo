#!/usr/bin/env python
"""

Cozmo animation manipulation tool.

Examples:

- view clips and keyframes in an animation file

    pycozmo_anim.py info anim_bored_01.bin

- convert a FlatBuffers (.bin) animation to JSON format

    pycozmo_anim.py json anim_bored_01.bin

- convert a JSON animation to FlatBuffers format

    pycozmo_anim.py bin anim_bored_01.json

- export procedural face images from an animation file

    pycozmo_anim.py images anim_bored_01.bin

"""

import sys
import os
import argparse
import struct
import json
from collections import Counter

import pycozmo


def do_info(args) -> None:
    ifspec = args.input

    try:
        clips = pycozmo.anim_encoder.AnimClips.from_fb_file(ifspec)
    except (OSError, struct.error) as e:
        print("ERROR: Failed to load animation file '{}'. {}".format(ifspec, e))
        sys.exit(1)

    for i, clip in enumerate(clips.clips):
        print("{} (index {})".format(clip.name, i))
        counts = Counter([type(keyframe).__name__ for keyframe in clip.keyframes])
        for k, v in sorted(counts.items()):
            print("\t{}: {}".format(k, v))


def do_json(args) -> None:
    ifspec = args.input
    ofspec = args.output
    if not ofspec:
        ofspec = os.path.splitext(ifspec)[0] + '.json'

    try:
        clips = pycozmo.anim_encoder.AnimClips.from_fb_file(ifspec)
    except (OSError, struct.error) as e:
        print("ERROR: Failed to load animation file '{}'. {}".format(ifspec, e))
        sys.exit(1)

    try:
        clips.to_json_file(ofspec)
    except OSError as e:
        print("ERROR: Failed to write animation file '{}'. {}".format(ifspec, e))
        sys.exit(1)


def do_bin(args) -> None:
    ifspec = args.input
    ofspec = args.output
    if not ofspec:
        ofspec = os.path.splitext(ifspec)[0] + '.bin'

    try:
        clips = pycozmo.anim_encoder.AnimClips.from_json_file(ifspec)
    except (OSError, json.decoder.JSONDecodeError) as e:
        print("ERROR: Failed to load animation file '{}'. {}".format(ifspec, e))
        sys.exit(1)

    try:
        clips.to_fb_file(ofspec)
    except OSError as e:
        print("ERROR: Failed to write animation file '{}'. {}".format(ifspec, e))
        sys.exit(1)


def write_procedural_face(keyframe: pycozmo.anim_encoder.AnimProceduralFace, fspec: str) -> None:
    im = pycozmo.anim.PreprocessedClip.keyframe_to_im(keyframe)
    try:
        im.save(fspec, "PNG")
    except OSError as e:
        print("ERROR: Failed to write procedural face image '{}'. {}".format(fspec, e))
        sys.exit(1)


def do_images(args) -> None:
    ifspec = args.input
    prefix = args.prefix
    if not prefix:
        prefix = os.path.splitext(ifspec)[0]

    try:
        clips = pycozmo.anim_encoder.AnimClips.from_fb_file(ifspec)
    except (OSError, struct.error) as e:
        print("ERROR: Failed to load animation file '{}'. {}".format(ifspec, e))
        sys.exit(1)

    for clip in clips.clips:
        for keyframe in clip.keyframes:
            if isinstance(keyframe, pycozmo.anim_encoder.AnimProceduralFace):
                ofspec = "{}-{}-{:06d}.png".format(prefix, clip.name, keyframe.trigger_time_ms)
                write_procedural_face(keyframe, ofspec)


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    subparser = subparsers.add_parser("info", help="view clips and keyframes in an animation file")
    subparser.add_argument("input", help="input file specification")

    subparser = subparsers.add_parser(
        "json", help="convert an animation in FlatBuffers format to JSON format")
    subparser.add_argument("input", help="input file specification")
    subparser.add_argument("-o", "--output", help="output file specification")

    subparser = subparsers.add_parser(
        "bin", help="convert an animation in JSON format to FlatBuffers format.")
    subparser.add_argument("input", help="input file specification")
    subparser.add_argument("-o", "--output", help="output file specification")

    subparser = subparsers.add_parser("images", help="export procedural face images from an animation file")
    subparser.add_argument("input", help="input file specification")
    subparser.add_argument("-p", "--prefix", help="output file specification prefix")

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    cmd_func = getattr(sys.modules[__name__], "do_" + args.cmd)
    cmd_func(args)


if __name__ == '__main__':
    main()
