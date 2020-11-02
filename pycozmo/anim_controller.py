
import time
import datetime
from threading import Thread, Lock
from collections import deque

from . import logger
from . import protocol_encoder


class AnimationQueue:

    MAXLEN = 4500   # ~2.5 min of frames

    def __init__(self):
        self.mutex = Lock()
        self.audio_queue = deque(maxlen=self.MAXLEN)
        self.image_queue = deque(maxlen=self.MAXLEN)
        self.other_queue = deque(maxlen=self.MAXLEN)

    def join(self):
        pass

    def is_empty(self):
        with self.mutex:
            return not len(self.audio_queue) and \
                   not len(self.image_queue) and \
                   not len(self.other_queue)

    def put(self, item):
        pass

    def get(self):
        self.audio_queue.popleft()


class AnimationController:

    def __init__(self, cli):
        self.cli = cli
        self.thread = None
        self.stop_flag = False
        self.num_audio_frames_played = -1

    def start(self):
        self.thread = Thread(daemon=True, name=__class__.__name__, target=self._run)
        self.stop_flag = False
        self.thread.start()
        self.cli.conn.add_handler(protocol_encoder.AnimationState, self._on_animation_state)
        self.cli.conn.add_handler(protocol_encoder.Keyframe, self._on_keyframe)

    def stop(self):
        self.stop_flag = True
        self.thread.join()

    def _on_animation_state(self, cli, pkt: protocol_encoder.AnimationState):
        # logger.info(pkt)
        # logger.info("+ {}".format(pkt.num_audio_frames_played))
        self.num_audio_frames_played = pkt.num_audio_frames_played
        pass

    def _on_keyframe(self, cli, pkt: protocol_encoder.Keyframe):
        # logger.info(pkt)
        logger.info("** K **")
        pass

    def _run(self):
        logger.debug("Animation controller started...")

        # Enable animation playback and AnimationState events. Requires Enable (0x25).
        pkt = protocol_encoder.EnableAnimationState()
        self.cli.conn.send(pkt)

        num_audio_frames = 0
        next_frame = datetime.datetime.now()

        while not self.stop_flag:

            while True:
                now = datetime.datetime.now()
                if now >= next_frame:  # or (num_audio_frames - self.num_audio_frames_played) < 2:
                    break
                time.sleep(0.010)
                # logger.info(".")
            if now - next_frame > datetime.timedelta(seconds=1.0):
                # More than 30 frames behind.
                next_frame = now
            next_frame += datetime.timedelta(seconds=1/30)

            pkt = protocol_encoder.NextFrame()
            self.cli.conn.send(pkt)
            pkt = protocol_encoder.DisplayImage(b"\x3f\x3f")
            self.cli.conn.send(pkt)

            num_audio_frames += 1
            # logger.info(num_audio_frames)

        logger.debug("Animation controller stopped...")
