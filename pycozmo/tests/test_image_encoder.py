
import unittest

from pycozmo.image_encoder import ImageEncoder, str_to_image, ImageDecoder, image_to_str
from pycozmo.util import hex_dump, hex_load
from pycozmo.tests.image_encoder_fixtures import FIXTURES


class TestImageEncoder(unittest.TestCase):

    @staticmethod
    def _encode(sim: str) -> str:
        im = str_to_image(sim)
        encoder = ImageEncoder(im)
        buf = encoder.encode()
        res = hex_dump(buf)
        return res

    def assertSameImage(self, sim: str, seq: str) -> None:
        buffer = hex_load(seq)
        decoder = ImageDecoder(buffer)
        decoder.decode()
        actual = image_to_str(decoder.image)
        self.assertEqual(sim.strip(), actual.strip())

    def test_blank(self):
        fixture = FIXTURES["blank"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_fill_screen(self):
        fixture = FIXTURES["fill_screen"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_fill_screen2(self):
        fixture = FIXTURES["fill_screen2"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_top_left(self):
        fixture = FIXTURES["top_left"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does 82
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_top_left_5(self):
        fixture = FIXTURES["top_left_5"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does 82
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_top_left_1_8(self):
        fixture = FIXTURES["top_left_1_8"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_top_left_line(self):
        fixture = FIXTURES["top_left_line"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_top_line(self):
        fixture = FIXTURES["top_line"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does "82:7f:7e". Why 82???
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_bottom_line(self):
        fixture = FIXTURES["bottom_line"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does "f8:82:7f:7e". Why 82???
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_left_line(self):
        fixture = FIXTURES["left_line"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_right_line(self):
        fixture = FIXTURES["right_line"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_columns(self):
        fixture = FIXTURES["columns"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does fd. Why?
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_rect(self):
        fixture = FIXTURES["rect"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does:
        # expected = "fe:82:f4:82:7f:7c:fe"
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_rect2(self):
        fixture = FIXTURES["rect2"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does:
        # expected = "00:fe:82:f4:82:7f:7a:fe:00"
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_rect3(self):
        fixture = FIXTURES["rect3"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does:
        # expected = "01:80:f6:80:80:82:ec:82:7f:78:80:f6:01"
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_rect4(self):
        fixture = FIXTURES["rect4"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does
        # expected = "fe:82:f4:82:fe:86:ec:86:7f:78:fe:82:f4:82:fe"
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_diagonal(self):
        fixture = FIXTURES["diagonal"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does
        # expected = "82:42:80:82:42:84:82:42:88:82:42:8c:82:42:90:82:42:94:82:42:98:82:42:9c:82:42:a0:82:42:a4:82:42:" \
        #            "a8:82:42:ac:82:42:b0:82:42:b4:82:42:b8:82:42:bc:82:42:c0:82:42:c4:82:42:c8:82:42:cc:82:42:d0:82:" \
        #            "42:d4:82:42:d8:82:42:dc:82:42:e0:82:42:e4:82:42:e8:82:42:ec:82:42:f0:82:42:f4:82:42:f8:82:42"
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_diagonal2(self):
        fixture = FIXTURES["diagonal2"]
        sim = fixture["image"]
        expected = fixture["seq"]
        # TODO: Cozmo does:
        # expected = "f8:82:42:f4:82:42:f0:82:42:ec:82:42:e8:82:42:e4:82:42:e0:82:42:dc:82:42:d8:82:42:d4:82:42:d0:82:" \
        #            "42:cc:82:42:c8:82:42:c4:82:42:c0:82:42:bc:82:42:b8:82:42:b4:82:42:b0:82:42:ac:82:42:a8:82:42:a4:" \
        #            "82:42:a0:82:42:9c:82:42:98:82:42:94:82:42:90:82:42:8c:82:42:88:82:42:84:82:42:80:82:42:82:42"
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_blocks(self):
        fixture = FIXTURES["blocks"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_pycozmo(self):
        fixture = FIXTURES["pycozmo"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)
