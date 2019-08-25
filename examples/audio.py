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

    while cli.state != pycozmo.Client.CONNECTED:
        time.sleep(0.2)

    cli.send_enable()
    time.sleep(1)

    done = False
    while not done:
        frame = f.readframes(744)
        if len(frame) < 744:
            done = True
            frame = frame.ljust(744, b"\x80")

        pkt = pycozmo.protocol_encoder.OutputAudio(frame)
        cli.send(pkt)
        time.sleep(0.033742)

    cli.send_disconnect()
    time.sleep(1)


if __name__ == '__main__':
    main()
