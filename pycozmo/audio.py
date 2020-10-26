"""

Cozmo audio encoding.

References:
    - https://en.wikipedia.org/wiki/%CE%9C-law_algorithm
    - http://dystopiancode.blogspot.com/2012/02/pcm-law-and-u-law-companding-algorithms.html

"""

from typing import List
import struct
import wave
from threading import Thread

from . import conn
from . import protocol_encoder
from . import anim
from . import util


__all__ = [
    "AudioManager",

    "load_wav",
]


MULAW_MAX = 0x7FFF
MULAW_BIAS = 132


class AudioManager:
    """
    This class takes care of reading audio files and generating the OutputAudio messages sent to
    cozmo.

    The play() method can be used to play an audio file or list of OutputAudio messages.

    Args:
        connection (ClientConnection): client managing the communication with the robot
    """

    def __init__(self, connection: conn.ClientConnection) -> None:
        self.conn = connection
        self._stop = False
        self.thread = None
        self.audio_stream = []

    def start_stream(self) -> None:
        self._stop = False
        if not self.thread:
            self.thread = Thread(target=self.run, name=__class__.__name__)
            self.thread.start()

    def stop(self) -> None:
        self._stop = True
        if self.thread:
            self.thread.join()
            self.thread = None
        self.audio_stream = []

    def run(self) -> None:
        timer = util.FPSTimer(anim.FRAME_RATE)
        while len(self.audio_stream) > 0 and not self._stop:
            pkt = self.audio_stream.pop(0)
            self.conn.send(pkt)
            timer.sleep()

    def play(self, audio) -> None:
        if audio and isinstance(audio, list) and isinstance(audio[0], protocol_encoder.OutputAudio):
            self.audio_stream += audio
        else:
            raise TypeError('Invalid audio: {}'.format(type(audio)))

        self.start_stream()

    def play_file(self, filename: str) -> None:
        if isinstance(filename, str):
            if '.wav' == filename[-4:]:
                self.play(load_wav(filename))
            else:
                raise ValueError(
                    'Only WAV files are supported, invalid audio file: {}'.format(filename))
        else:
            raise TypeError('Expected path to audio file, invalid argument: {}'.format(filename))

        self.start_stream()

    def wait_until_complete(self) -> None:
        if self.thread:
            self.thread.join()
            self.thread = None


def load_wav(filename: str) -> List[protocol_encoder.OutputAudio]:
    with wave.open(filename, "r") as w:
        sampwidth = w.getsampwidth()
        framerate = w.getframerate()
        if sampwidth != 2 or (framerate != 22050 and framerate != 48000):
            raise ValueError('Invalid audio format, only 16 bit samples are supported, ' +
                             'with 22050Hz or 48000Hz frame rates.')

        ratediv = 2 if framerate == 48000 else 1
        channels = w.getnchannels()
        done = False
        pkt_list = []

        while not done:
            frame = bytes_to_cozmo(w.readframes(744 * ratediv), ratediv, channels)
            if len(frame) < 744:
                frame += [0] * (744 - len(frame))
                done = True

            pkt_list.append(protocol_encoder.OutputAudio(frame))
        return pkt_list


def bytes_to_cozmo(byte_string: bytes, rate_correction: int, channels: int) -> List[int]:
    out = []
    n = channels * rate_correction
    bs = struct.unpack('{}h'.format(int(len(byte_string) / 2)), byte_string)[0::n]
    for s in bs:
        out.append(u_law_encoding(s))
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
