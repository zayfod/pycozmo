"""

Cozmo audio encoding.

References:
    - https://en.wikipedia.org/wiki/%CE%9C-law_algorithm
    - http://dystopiancode.blogspot.com/2012/02/pcm-law-and-u-law-companding-algorithms.html

"""

from typing import List
import struct
import wave

from . import protocol_encoder


__all__ = [
    "load_wav",
]


MULAW_MAX = 0x7FFF
MULAW_BIAS = 132


def load_wav(filename: str) -> List[protocol_encoder.OutputAudio]:
    """ Load a WAVE file into a list of OutputAudio packets. """
    with wave.open(filename, "r") as w:
        sampwidth = w.getsampwidth()
        framerate = w.getframerate()
        if sampwidth != 2 or (framerate != 22050 and framerate != 48000):
            raise ValueError('Invalid audio format, only 16 bit samples are supported, ' +
                             'with 22050Hz or 48000Hz frame rates.')

        ratediv = 2 if framerate == 48000 else 1
        channels = w.getnchannels()
        pkts = []

        while True:
            frame_in = w.readframes(744 * ratediv)
            if not frame_in:
                break
            frame_out = bytes_to_cozmo(frame_in, ratediv, channels)
            pkt = protocol_encoder.OutputAudio(samples=frame_out)
            pkts.append(pkt)
        return pkts


def bytes_to_cozmo(byte_string: bytes, rate_correction: int, channels: int) -> bytearray:
    """ Convert a 744 sample, 16-bit audio frame into a U-law encoded frame. """
    out = bytearray(744)
    n = channels * rate_correction
    bs = struct.unpack('{}h'.format(int(len(byte_string) / 2)), byte_string)[0::n]
    for i, s in enumerate(bs):
        out[i] = u_law_encoding(s)
    return out


def u_law_encoding(sample: int) -> int:
    """ U-law encode a 16-bit PCM sample. """
    mask = 0x4000
    position = 14
    sign = 0
    if sample < 0:
        sample = -sample
        sign = 0x80
    sample += MULAW_BIAS
    if sample > MULAW_MAX:
        sample = MULAW_MAX

    while (sample & mask) != mask and position >= 7:
        mask >>= 1
        position -= 1

    lsb = (sample >> (position - 4)) & 0x0f
    return -(~(sign | ((position - 7) << 4) | lsb))
