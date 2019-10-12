#!/usr/bin/env python

import time
import wave

import pycozmo


def pycozmo_program(cli: pycozmo.client.Client):
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

    pkt = pycozmo.protocol_encoder.SetRobotVolume(20000)
    cli.conn.send(pkt)

    done = False
    while not done:
        frame = f.readframes(744)
        if len(frame) < 744:
            done = True
            frame = frame.ljust(744, b"\x80")

        pkt = pycozmo.protocol_encoder.OutputAudio(frame)
        cli.conn.send(pkt)
        time.sleep(0.033742)


pycozmo.run_program(pycozmo_program)
