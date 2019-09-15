"""

Experimental code for reading Cozmo animations in .bin format.

Cozmo animations are stored in files/cozmo/cozmo_resources/assets/animations inside the Cozmo mobile application.

Declarations of the animation data structure seem to be available in files/cozmo/cozmo_resources/config/cozmo_anim.fbs

"""

from . import protocol_utils
from . import util


__all__ = [
    "AnimClip",
    "AnimBinReader",
]


class AnimClip(object):

    def __init__(self, name: str):
        self.name = name


class AnimBinReader(object):

    def __init__(self):
        self.anim_clips = []

    def read_keyframes(self, buf):
        reader = protocol_utils.BinaryReader(buf)

        buf2_len = reader.read("L")
        assert buf2_len == 36
        buf2 = reader.read_farray("B", buf2_len)
        # print(util.hex_dump(bytes(buf2)))
        # print(util.hex_dump(reader.buffer[reader.tell():]))

    def read_sub_anim_data(self, name, buf):
        """ Read sub animation data. """
        reader = protocol_utils.BinaryReader(buf)

        # What is this?
        buf2_len = reader.read("L")
        assert buf2_len == 4
        cnt = reader.read("L")
        # print("{:08x}".format(cnt))

        # Keyframes?
        buf2_len = reader.read("L")
        # print(buf2_len)
        buf2 = reader.read_farray("B", buf2_len)
        # print(util.hex_dump(bytes(buf2)))
        self.read_keyframes(bytes(buf2))

        # ???
        buf2_len = reader.read("L")
        # print("{:08x}".format(buf2_len))
        buf2 = reader.read_farray("B", buf2_len)
        # print(util.hex_dump(bytes(buf2)))

        # 0-16 B remain. What are these?

        anim_clip = AnimClip(name)
        self.anim_clips.append(anim_clip)

    def read_sub_anim(self, buf, cnt):
        """ Read sub animation. """
        reader = protocol_utils.BinaryReader(buf)

        # Sub animations
        buf2_len = reader.read("L")
        buf2 = reader.read_farray("B", buf2_len)
        if cnt > 1:
            self.read_sub_anim(bytes(buf2), cnt - 1)
        else:
            # What is this?
            pass

        # Animation data
        buf2_len = reader.read("L")
        buf2 = reader.read_farray("B", buf2_len - 4)  # The -4 is weird but otherwise the name length is eaten up

        # Animation name
        buf2_len = reader.read("L")
        name = bytes(reader.read_farray("B", buf2_len)).decode("utf-8")

        self.read_sub_anim_data(name, bytes(buf2))

    def read_main_anim_data(self, name, buf):
        """ Read main animation data. """
        reader = protocol_utils.BinaryReader(buf)

        # Always 28 B.
        buf2_len = reader.read("L")
        assert buf2_len == 28
        buf2 = reader.read_farray("B", buf2_len)

        # Keyframes?
        buf2_len = reader.read("L")
        buf2 = reader.read_farray("B", buf2_len)
        # print(util.hex_dump(bytes(buf2)))
        self.read_keyframes(bytes(buf2))

        # ???
        buf2_len = reader.read("L")
        buf2 = reader.read_farray("B", buf2_len)
        # print(util.hex_dump(bytes(buf2)))

        # 0-16 B remain. What are these?

        anim_clip = AnimClip(name)
        self.anim_clips.append(anim_clip)

    def read_file(self, fspec):
        """ Read an animation .bin file. """
        with open(fspec, "rb") as f:
            buf = f.read()
            reader = protocol_utils.BinaryReader(buf)

            # Header?
            buf2_len = reader.read("L")
            buf2 = reader.read_farray("B", buf2_len)
            assert buf2 == (0, 0, 0, 0, 0, 0, 6, 0, 8, 0, 4, 0, 6, 0, 0, 0) or \
                buf2 == (0, 0, 6, 0, 8, 0, 4, 0, 6, 0, 0, 0)

            # Count of animations
            buf2_len = reader.read("L")
            assert buf2_len == 4
            cnt = reader.read("L")
            # print(cnt)

            # Sub animations
            buf2_len = reader.read("L")
            buf2 = reader.read_farray("B", buf2_len)
            if cnt > 1:
                self.read_sub_anim(bytes(buf2), cnt - 1)
            else:
                # What is this?
                pass

            # Main animation
            buf2_len = reader.read("L")
            buf2 = reader.read_farray("B", buf2_len - 4)  # The -4 is weird but otherwise the name length is eaten up

            # Main animation name
            buf2_len = reader.read("L")
            name = bytes(reader.read_farray("B", buf2_len)).decode("utf-8")

            self.read_main_anim_data(name, bytes(buf2))

        return self.anim_clips
