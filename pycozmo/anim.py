"""

Experimental code for reading Cozmo animations in .bin format.

Cozmo animations are stored in files/cozmo/cozmo_resources/assets/animations inside the Cozmo mobile application.

"""

from . import protocol_utils


def read_anim(buf):
    """ Read animation section. """
    reader = protocol_utils.BinaryReader(buf)

    # Always 28 B.
    l = reader.read("L")
    assert l == 28
    fa = reader.read_farray("B", l)
    # print(fa)

    l = reader.read("L")
    print(l)
    fa = reader.read_farray("B", l)
    # print(bytes(fa))

    l = reader.read("L")
    print(l)
    fa = reader.read_farray("B", l)
    # print(bytes(fa))

    # print(len(reader.buffer) - reader.tell())
    # print(reader.buffer[reader._index:])


def read_bin(fspec):
    """ Read a .bin file. """
    with open(fspec, "rb") as f:
        buf = f.read()
        reader = protocol_utils.BinaryReader(buf)

        # Header?
        l = reader.read("L")
        fa = reader.read_farray("B", l)
        assert fa == (0, 0, 0, 0, 0, 0, 6, 0, 8, 0, 4, 0, 6, 0, 0, 0) or fa == (0, 0, 6, 0, 8, 0, 4, 0, 6, 0, 0, 0)

        # Count of some sort?
        l = reader.read("L")
        assert l == 4
        cnt = reader.read("L")
        # print(cnt)

        l = reader.read("L")
        # print(l)
        fa = reader.read_farray("B", l)
        # print(bytes(fa))

        l = reader.read("L")
        # print(l)
        fa = reader.read_farray("B", l - 4)     # The -4 here is weird but otherwise the name length is eaten up
        # print(bytes(fa))
        read_anim(bytes(fa))

        # Something similar to the name of the file, without .bin extension, padded with 0s to a 32-bin boundary?
        l = reader.read("L")
        name = reader.buffer[reader._index:].strip(b"\0").decode("utf-8")
        # print(name)
        assert(l == len(name))
