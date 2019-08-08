
import pycozmo


def main():
    with open("../pycozmo/protocol_encoder.py", "w") as f:
        gen = pycozmo.protocol_generator.ProtocolGenerator(f)
        gen.generate()


if __name__ == '__main__':
    main()
