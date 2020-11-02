
from typing import List, Tuple, Any, Optional, Iterable
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
        self.pkt_queue = deque(maxlen=self.MAXLEN)

    def is_empty(self):
        with self.lock:
            return not len(self.audio_queue) and \
                   not len(self.image_queue) and \
                   not len(self.pkt_queue)

    def put_audio(self, pkts: List[protocol_encoder.OutputAudio]) -> None:
        with self.lock:
            self.audio_queue.extend(pkts)

    def put_image(self, pkt: protocol_encoder.DisplayImage) -> None:
        with self.lock:
            self.image_queue.append(pkt)

    def put_anim_frame(
            self,
            audio_pkt: Optional[protocol_encoder.OutputAudio],
            image_pkt: Optional[protocol_encoder.DisplayImage],
            pkts: Optional[Iterable[protocol_encoder.Packet]]) -> None:
        with self.lock:
            self.audio_queue.append(audio_pkt)
            self.image_queue.append(image_pkt)
            self.pkt_queue.append(pkts)

    def get(self) -> Tuple[bytes, bytes, Tuple[Any]]:
        with self.lock:
            # Audio
            try:
                audio_pkt = self.audio_queue.popleft()
            except IndexError:
                audio_pkt = None
            # Image
            try:
                image_pkt = self.image_queue.popleft()
            except IndexError:
                image_pkt = None
            # Action
            try:
                pkts = self.pkt_queue.popleft()
            except IndexError:
                pkts = None

        return audio_pkt, image_pkt, pkts


class AnimationController:

    def __init__(self, cli):
        self.cli = cli
        self.thread = None
        self.stop_flag = False
        self.queue = AnimationQueue()
        self.num_audio_frames_played = -1
        self.playing_audio = False
        self.last_image_pkt = protocol_encoder.DisplayImage(image=b"\x3f\x3f")

    def _clear_last_image_pkt(self):
        self.last_image_pkt = protocol_encoder.DisplayImage(image=b"\x3f\x3f")

    def start(self):
        self.thread = Thread(daemon=True, name=__class__.__name__, target=self._run)
        self.stop_flag = False
        self.thread.start()
        self.cli.add_handler(protocol_encoder.AnimationState, self._on_animation_state)
        self.cli.add_handler(protocol_encoder.Keyframe, self._on_keyframe)
        self.cli.add_handler(protocol_encoder.AnimationStarted, self._on_animation_started)
        self.cli.add_handler(protocol_encoder.AnimationEnded, self._on_animation_ended)
        self.cli.add_handler(event.EvtRobotAnimatingChange, self._on_animating_change)
        self.cli.add_handler(event.EvtRobotAnimBufferFullChange, self._on_anim_buffer_full_change)
        self.cli.add_handler(event.EvtRobotAnimatingIdleChange, self._on_amimating_idle_change)

    def stop(self):
        self.stop_flag = True
        self.thread.join()
        self.thread = None

    def _on_animation_state(self, cli, pkt: protocol_encoder.AnimationState):
        self.num_audio_frames_played = pkt.num_audio_frames_played

    def _on_keyframe(self, cli, pkt: protocol_encoder.Keyframe):
        pass

    def _on_animation_started(self, cli, pkt: protocol_encoder.AnimationStarted):
        pass

    def _on_animation_ended(self, cli, pkt: protocol_encoder.AnimationEnded):
        self._clear_last_image_pkt()
        self.cli.conn.post_event(event.EvtAnimationCompleted, self.cli)

    def _on_animating_change(self):
        pass

    def _on_anim_buffer_full_change(self):
        pass

    def _on_amimating_idle_change(self):
        pass

    def _run(self):
        logger.debug("Animation controller started...")

        # Enable animation playback and AnimationState events. Requires Enable (0x25).
        pkt = protocol_encoder.EnableAnimationState()
        self.cli.conn.send(pkt)

        num_audio_frames = 0

        timer = util.FPSTimer(anim.FRAME_RATE)
        while not self.stop_flag:

            audio_pkt, image_pkt, pkts = self.queue.get()

            if audio_pkt:
                if not self.playing_audio:
                    self.playing_audio = True
            else:
                audio_pkt = protocol_encoder.OutputSilence()
                if self.playing_audio:
                    self.playing_audio = False
                    self.cli.conn.post_event(event.EvtAudioCompleted, self.cli)
            self.cli.conn.send(audio_pkt)

            if image_pkt:
                self.cli.conn.send(image_pkt)
                self.last_image_pkt = image_pkt
            else:
                # If not refreshed, the robot stops displaying image after 30 s.
                self.cli.conn.send(self.last_image_pkt)

            if pkts:
                for pkt in pkts:
                    self.cli.conn.send(pkt)

            num_audio_frames += 1

            timer.sleep()

        logger.debug("Animation controller stopped...")

    def play_audio(self, pkts: List[protocol_encoder.OutputAudio]) -> None:
        self.queue.put_audio(pkts)

    def display_image(self, pkt: protocol_encoder.DisplayImage) -> None:
        self.queue.put_image(pkt)

    def play_anim_frame(
            self,
            audio_pkt: Optional[protocol_encoder.OutputAudio],
            image_pkt: Optional[protocol_encoder.DisplayImage],
            pkts: Optional[Iterable[protocol_encoder.Packet]]) -> None:
        self.queue.put_anim_frame(audio_pkt, image_pkt, pkts)
