import struct
import time
import wave
from datetime import datetime, timedelta
from threading import Thread, Lock

from .conn import ClientConnection
from .protocol_encoder import OutputAudio

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
        self.audio_stream = []

    def start_stream(self):
        self.stop = False
        if not self.thread.is_alive():
            self.thread = Thread(target=self.run, name=__class__.__name__)
            self.thread.start()

    def stop(self) -> None:
        self.stop = True
        self.thread.join()
        self.audio_stream = []

    def run(self) -> None:
        while len(self.audio_stream) > 0 and not self.stop:
            next_trigger_time = datetime.now() + timedelta(seconds=MIN_WAIT)
            with self.lock:
                pkt = self.audio_stream.pop(0)
            self.conn.send(pkt)

            resting_time = (next_trigger_time - datetime.now()).total_seconds()
            if resting_time > 0:
                time.sleep(resting_time)

    def play(self, audio):
        if audio and isinstance(audio, list) and isinstance(audio[0], OutputAudio):
            with self.lock:
                self.audio_stream += audio
        else:
            raise TypeError('Invalid audio: {}'.format(type(audio)))

        self.start_stream()

    def play_file(self, filename):
        if isinstance(filename, str):
            if '.wav' == filename[-4:]:
                self.play(load_wav(filename))
            else:
                raise ValueError(
                    'Only WAV files are supported, invalid audio file: {}'.format(filename))
        else:
            raise TypeError('Expected path to audio file, invalid argument: {}'.format(filename))

        self.start_stream()

    def wait_until_complete(self):
        self.thread.join()

    def is_running(self):
        return self.thread.is_alive()


def load_wav(self, filename: str):
    with wave.open(filename, "r") as w:
        sampwidth = w.getsampwidth()
        framerate = w.getframerate()
        if sampwidth != 2 or (framerate != 22050 and framerate != 48000):
            raise TypeError('Invalid audio format, only 16 bit samples are supported,' +
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

            pkt_list.append(OutputAudio(frame))
        return pkt_list


def bytes_to_cozmo(byte_string: bytes, rate_correction: int, channels: int):
    out = []
    n = channels * rate_correction
    bs = struct.unpack('{}h'.format(int(len(byte_string) / 2)), byte_string)[0::n]
    for s in bs:
        out.append(u_law_encoding(s))
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

    while (sample & mask) != mask and position >= 7:
        mask >>= 1
        position -= 1

    lsb = (sample >> (position - 4)) & 0x0f
    return -(~(sign | ((position - 7) << 4) | lsb))
