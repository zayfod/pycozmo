#!/usr/bin/env python

import time
import wave

import pycozmo


def main():
    f = wave.open("hello.wav", "rb")
    sampwidth = f.getsampwidth()
    print("Sample width: {} byte(s)".format(sampwidth))
    rate = f.getframerate()
    print("Sampling rate: {} Hz".format(rate))
    channels = f.getnchannels()
    print("Channels: {}".format(channels))

    assert sampwidth == 1
    assert rate == 22050
    assert channels == 1

    cli = pycozmo.Client()
    cli.start()
    cli.connect()
    cli.wait_for_robot()

    pkt = pycozmo.protocol_encoder.SetRobotVolume(20000)
    cli.send(pkt)

    done = False
    while not done:
        frame = f.readframes(744)
        if len(frame) < 744:
            done = True
            frame = frame.ljust(744, b"\x80")

        pkt = pycozmo.protocol_encoder.OutputAudio(frame)
        cli.send(pkt)
        time.sleep(0.033742)

    cli.disconnect()
    cli.stop()


if __name__ == '__main__':
    main()
