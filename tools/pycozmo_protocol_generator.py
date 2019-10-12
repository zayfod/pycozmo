
from io import StringIO
import shutil
import pycozmo


def main():
    buf = StringIO()
    gen = pycozmo.protocol_generator.ProtocolGenerator(buf)
    gen.generate()

    buf.seek(0)
    with open("../pycozmo/protocol_encoder.py", "w") as f:
        shutil.copyfileobj(buf, f)


if __name__ == '__main__':
    main()
