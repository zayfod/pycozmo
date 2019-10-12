
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
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_top_left_5(self):
        fixture = FIXTURES["top_left_5"]
        sim = fixture["image"]
        expected = fixture["seq"]
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
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_bottom_line(self):
        fixture = FIXTURES["bottom_line"]
        sim = fixture["image"]
        expected = fixture["seq"]
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
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_rect(self):
        fixture = FIXTURES["rect"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_rect2(self):
        fixture = FIXTURES["rect2"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_rect3(self):
        fixture = FIXTURES["rect3"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_rect4(self):
        fixture = FIXTURES["rect4"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_diagonal(self):
        fixture = FIXTURES["diagonal"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_diagonal2(self):
        fixture = FIXTURES["diagonal2"]
        sim = fixture["image"]
        expected = fixture["seq"]
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

    def test_chessboard_tl(self):
        fixture = FIXTURES["chessboard_tl"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_chessboard_bl(self):
        fixture = FIXTURES["chessboard_bl"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_chessboard_tr(self):
        fixture = FIXTURES["chessboard_tr"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_chessboard_br(self):
        fixture = FIXTURES["chessboard_br"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_chessboard2_tl(self):
        fixture = FIXTURES["chessboard2_tl"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_chessboard2_bl(self):
        fixture = FIXTURES["chessboard2_bl"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_chessboard2_tr(self):
        fixture = FIXTURES["chessboard2_tr"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)

    def test_chessboard2_br(self):
        fixture = FIXTURES["chessboard2_br"]
        sim = fixture["image"]
        expected = fixture["seq"]
        actual = self._encode(sim)
        self.assertEqual(expected, actual)
        self.assertSameImage(sim, actual)
