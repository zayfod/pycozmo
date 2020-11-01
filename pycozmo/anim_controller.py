
from typing import List, Tuple
from threading import Thread, Lock
from collections import deque

from . import logger
from . import protocol_encoder
from . import util
from . import anim
from . import event


class AnimationQueue:

    MAXLEN = 4500   # ~2.5 min of frames

    def __init__(self):
        self.lock = Lock()
        self.audio_queue = deque(maxlen=self.MAXLEN)
        self.image_queue = deque(maxlen=self.MAXLEN)
        self.other_queue = deque(maxlen=self.MAXLEN)

    def join(self):
        pass

    def is_empty(self):
        with self.lock:
            return not len(self.audio_queue) and \
                   not len(self.image_queue) and \
                   not len(self.other_queue)

    def put_audio(self, sample_list: List[bytes]) -> None:
        with self.lock:
            self.audio_queue.extend(sample_list)

    def put_image(self, buf: bytes) -> None:
        with self.lock:
            self.image_queue.append(buf)

    def get(self) -> Tuple[bytes, bytes]:
        with self.lock:
            # Audio
            try:
                samples = self.audio_queue.popleft()
            except IndexError:
                samples = None
            # Image
            try:
                image = self.image_queue.popleft()
            except IndexError:
                image = None
        return samples, image


class AnimationController:

    def __init__(self, cli):
        self.cli = cli
        self.thread = None
        self.stop_flag = False
        self.queue = AnimationQueue()
        self.num_audio_frames_played = -1
        self.playing_audio = False
        self.last_image = protocol_encoder.DisplayImage(image=b"\x3f\x3f")

    def start(self):
        self.thread = Thread(daemon=True, name=__class__.__name__, target=self._run)
        self.stop_flag = False
        self.thread.start()
        self.cli.add_handler(protocol_encoder.AnimationState, self._on_animation_state)
        self.cli.add_handler(protocol_encoder.Keyframe, self._on_keyframe)

    def stop(self):
        self.stop_flag = True
        self.thread.join()
        self.thread = None

    def _on_animation_state(self, cli, pkt: protocol_encoder.AnimationState):
        self.num_audio_frames_played = pkt.num_audio_frames_played
        pass

    def _on_keyframe(self, cli, pkt: protocol_encoder.Keyframe):
        pass

    def _run(self):
        logger.debug("Animation controller started...")

        # Enable animation playback and AnimationState events. Requires Enable (0x25).
        pkt = protocol_encoder.EnableAnimationState()
        self.cli.conn.send(pkt)

        num_audio_frames = 0

        timer = util.FPSTimer(anim.FRAME_RATE)
        while not self.stop_flag:

            samples, image = self.queue.get()

            if samples:
                pkt = protocol_encoder.OutputAudio(samples=samples)
                if not self.playing_audio:
                    self.playing_audio = True
            else:
                pkt = protocol_encoder.NextFrame()
                if self.playing_audio:
                    self.playing_audio = False
                    self.cli.conn.post_event(event.EvtAudioCompleted, self.cli)
            self.cli.conn.send(pkt)

            if image:
                pkt = protocol_encoder.DisplayImage(image=image)
                self.cli.conn.send(pkt)
                self.last_image = pkt
            else:
                # If not refreshed, the robot stops displaying image after 30 s.
                self.cli.conn.send(self.last_image)

            num_audio_frames += 1

            timer.sleep()

        logger.debug("Animation controller stopped...")

    def play_audio(self, sample_list: List[bytes]) -> None:
        self.queue.put_audio(sample_list)

    def display_image(self, buf: bytes) -> None:
        self.queue.put_image(buf)

    def play_anim(self, ppclip: anim.PreprocessedClip) -> None:
        # TODO: See anim.PreprocessedClip.play()
        pass
