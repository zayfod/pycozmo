import struct
import time
import wave
from datetime import datetime, timedelta
from threading import Thread, Lock

from .conn import ClientConnection
from .protocol_encoder import OutputAudio, Keyframe

MIN_WAIT = 0.033

class AudioManager():
    """
    This class takes care of reading audio files and generating the OutputAudio messages sent to
    cozmo.

    The play() method can be used to play an audio file or list of OutputAudio messages.

    Args:
        conn (ClientConnection): client managing the communication with the robot
    """
    def __init__(self, conn: ClientConnection):
        self.stream = []
        self.stop = False
        self.conn = conn
        self.thread = Thread()
        self.lock = Lock()
        self.audio_gen = []

    def start(self):
        self.stop = False
        if not self.thread.is_alive():
            self.thread = Thread(target=self.run, name=__class__.__name__)
            self.thread.start()

    def stop(self) -> None:
        self.stop = True
        self.thread.join()
        self.audio_gen = []

    def run(self) -> None:
        while len(self.audio_gen) > 0:
            generator = []

            with self.lock:
                generator = self.audio_gen.pop(0)

            next_trigger_time = datetime.now()

            for pkt in generator:

                resting_time = (next_trigger_time - datetime.now()).total_seconds()
                if resting_time > 0:
                    time.sleep(resting_time)

                self.conn.send(pkt)

                next_trigger_time = datetime.now() + timedelta(seconds=MIN_WAIT)

                if self.stop:
                    return


    def _play_wav(self, filename: str):
        with wave.open(filename, "r") as w:
            sampwidth = w.getsampwidth()
            ratediv = 2 if w.getframerate() > 30000 else 1
            channels = w.getnchannels()
            done = False
            while not done:
                frame = bytes_to_cozmo(w.readframes(744 * ratediv),
                                            sampwidth, ratediv, channels)

                if len(frame) < 744:
                    frame += [0] * (744 - len(frame))
                    done = True

                yield OutputAudio(frame)

    def _play_packets(self, packets: list):
        for p in packets:
            yield p

    def play(self, audio):
        if '.wav' in audio:
            with self.lock:
                self.audio_gen.append( self._play_wav(audio) )
        elif isinstance(audio, list):
            with self.lock:
                self.audio_gen.append( self._play_packets(audio) )
        else:
            raise TypeError('Invalid audio type: {}'.format(type(audio)))

        self.start()

    def wait_until_complete(self):
        self.thread.join()

    def is_running(self):
        return self.thread.is_alive()


def bytes_to_cozmo(byte_string: bytes, sampwidth: int, rate_correction: int, channels: int):
    out = []
    n = channels * rate_correction
    if sampwidth == 1:
        # Usually, this will be a signed byte. It needs to be translated to something similar
        # to ulaw
        bs = struct.unpack('{}b'.format(len(byte_string)), byte_string)[0::n]
        for s in bs:
            out.append(s + 127 if s > 0 else -s)
    elif sampwidth == 2:
        bs = struct.unpack('{}h'.format(int(len(byte_string) / 2)), byte_string)[0::n]
        for s in bs:
            out.append(u_law_encoding(s))
    else:
        raise TypeError('Invalid sample width: {}\nOnly 8 and 16 bytes supported'
                        .format(sampwidth))
    return out


MULAW_MAX = 0x7FFF
MULAW_BIAS = 132
def u_law_encoding(sample):
    mask = 0x4000
    position = 14
    sign = 0
    lsb = 0
    if (sample < 0):
        sample = -sample
        sign = 0x80
    sample += MULAW_BIAS
    if (sample > MULAW_MAX):
        sample = MULAW_MAX

    while ((sample & mask) != mask and position >= 7):
        mask >>= 1
        position -= 1

    lsb = (sample >> (position - 4)) & 0x0f
    return -(~(sign | ((position - 7) << 4) | lsb))

