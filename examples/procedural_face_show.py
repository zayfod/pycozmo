#!/usr/bin/env python

import pycozmo


def main():
    # Render a 128x64 procedural face with default parameters.
    f = pycozmo.procedural_face.ProceduralFace()
    im = f.render()
    im.show()


if __name__ == '__main__':
    main()
