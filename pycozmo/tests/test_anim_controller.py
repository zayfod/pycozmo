
import unittest
from typing import Any

from PIL import Image

import pycozmo
from pycozmo import protocol_encoder
from pycozmo.anim_controller import AnimationController


BLANK = b"\x3f\x3f"
FACE = b"face"


class FakeConnection:
    """ Records sent packets instead of sending them to a robot. """

    def __init__(self) -> None:
        self.sent: list[protocol_encoder.Packet] = []
        self.events: list[Any] = []

    def send(self, pkt: protocol_encoder.Packet) -> None:
        self.sent.append(pkt)

    def post_event(self, evt: Any, *args: Any) -> None:
        self.events.append(evt)


class FakeClient:

    def __init__(self) -> None:
        self.conn = FakeConnection()


class MarkerFaceAnimationController(AnimationController):
    """ Uses a marker packet instead of rendering procedural faces. """

    def _get_face_image(self) -> protocol_encoder.DisplayImage:
        return protocol_encoder.DisplayImage(image=FACE)


class TestAnimationControllerImages(unittest.TestCase):

    def setUp(self) -> None:
        self.cli = FakeClient()
        self.controller = MarkerFaceAnimationController(self.cli)    # type: ignore[arg-type]
        self.controller.enable_animations(True)
        self.controller.enable_procedural_face(True)

    def run_frames(self, n: int) -> list[bytes]:
        """ Run n frames and return the displayed image data for each. """
        images = []
        for _ in range(n):
            self.cli.conn.sent.clear()
            self.controller._run_frame()
            frame_images = [pkt.image for pkt in self.cli.conn.sent
                            if isinstance(pkt, protocol_encoder.DisplayImage)]
            self.assertEqual(len(frame_images), 1)
            images.append(frame_images[0])
        return images

    def test_procedural_face(self) -> None:
        self.assertEqual(self.run_frames(3), [FACE, FACE, FACE])

    def test_displayed_image_is_kept(self) -> None:
        # Procedural face must not replace a displayed image.
        self.controller.display_image(protocol_encoder.DisplayImage(image=b"image"))
        self.assertEqual(self.run_frames(4), [b"image", b"image", b"image", b"image"])

    def test_clear_screen_resumes_procedural_face(self) -> None:
        self.controller.display_image(protocol_encoder.DisplayImage(image=b"image"))
        self.run_frames(2)
        self.controller.clear_screen()
        self.assertEqual(self.run_frames(3), [BLANK, FACE, FACE])

    def test_consecutive_images(self) -> None:
        self.controller.display_image(protocol_encoder.DisplayImage(image=b"image1"))
        self.controller.display_image(protocol_encoder.DisplayImage(image=b"image2"))
        self.assertEqual(self.run_frames(3), [b"image1", b"image2", b"image2"])

    def test_procedural_face_disabled(self) -> None:
        self.controller.enable_procedural_face(False)
        self.assertEqual(self.run_frames(2), [BLANK, BLANK])
        self.controller.display_image(protocol_encoder.DisplayImage(image=b"image"))
        self.assertEqual(self.run_frames(2), [b"image", b"image"])
        self.controller.clear_screen()
        self.assertEqual(self.run_frames(2), [BLANK, BLANK])

    def test_animations_disabled(self) -> None:
        self.controller.enable_animations(False)
        self.controller.display_image(protocol_encoder.DisplayImage(image=b"image"))
        self.controller._run_frame()
        self.assertEqual(self.cli.conn.sent, [])


class TestClientDisplayImage(unittest.TestCase):

    def setUp(self) -> None:
        # The client is not started, so nothing is sent.
        self.cli = pycozmo.Client()
        self.im = Image.new("1", (128, 32), color=0)

    def tearDown(self) -> None:
        self.cli.conn.sock.close()

    def queued_images(self) -> list[bytes]:
        images = []
        while self.cli.anim_controller.queue.image_queue:
            pkt = self.cli.anim_controller.queue.image_queue.popleft()
            assert pkt is not None
            images.append(pkt.image)
        return images

    def test_display_image(self) -> None:
        self.cli.display_image(self.im)
        self.assertTrue(self.cli.anim_controller.image_displayed)
        self.assertEqual(len(self.queued_images()), 1)

    def test_display_image_with_duration(self) -> None:
        self.cli.display_image(self.im, duration=0.01)
        # The image is followed by a blank screen, and procedural face may resume.
        self.assertFalse(self.cli.anim_controller.image_displayed)
        images = self.queued_images()
        self.assertEqual(len(images), 2)
        self.assertEqual(images[1], BLANK)

    def test_clear_screen(self) -> None:
        self.cli.display_image(self.im)
        self.cli.clear_screen()
        self.assertFalse(self.cli.anim_controller.image_displayed)
        self.assertEqual(self.queued_images()[-1], BLANK)
