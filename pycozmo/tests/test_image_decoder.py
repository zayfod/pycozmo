
import unittest

from pycozmo.image_encoder import ImageDecoder, image_to_str
from pycozmo.util import hex_load
from pycozmo.tests.image_encoder_fixtures import FIXTURES


class TestImageDecoder(unittest.TestCase):

    @staticmethod
    def _decode(seq: str) -> ImageDecoder:
        if isinstance(seq, str):
            buffer = hex_load(seq)
        else:
            buffer = bytes(seq)
        decoder = ImageDecoder(buffer)
        decoder.decode()
        return decoder

    def assertSameImage(self, expected: str, decoder: ImageDecoder) -> None:
        actual = image_to_str(decoder.image)
        self.assertEqual(expected.strip(), actual.strip())

    def test_blank(self):
        fixture = FIXTURES["blank"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)
        self.assertEqual(128, decoder.x)
        self.assertEqual(0, decoder.y)

    def test_fill_screen(self):
        fixture = FIXTURES["fill_screen"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)
        self.assertEqual(128, decoder.x)
        self.assertEqual(0, decoder.y)

    def test_fill_screen2(self):
        fixture = FIXTURES["fill_screen2"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)
        self.assertEqual(128, decoder.x)
        self.assertEqual(0, decoder.y)

    def test_top_left(self):
        fixture = FIXTURES["top_left"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_top_left_5(self):
        fixture = FIXTURES["top_left_5"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_top_left_1_8(self):
        fixture = FIXTURES["top_left_1_8"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_top_left_line(self):
        fixture = FIXTURES["top_left_line"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_top_line(self):
        fixture = FIXTURES["top_line"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_bottom_line(self):
        fixture = FIXTURES["bottom_line"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_left_line(self):
        fixture = FIXTURES["left_line"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_right_line(self):
        fixture = FIXTURES["right_line"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_columns(self):
        fixture = FIXTURES["columns"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_rect(self):
        fixture = FIXTURES["rect"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_rect2(self):
        fixture = FIXTURES["rect2"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_rect3(self):
        fixture = FIXTURES["rect3"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_rect4(self):
        fixture = FIXTURES["rect4"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_diagonal(self):
        fixture = FIXTURES["diagonal"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_diagonal2(self):
        fixture = FIXTURES["diagonal2"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_blocks(self):
        fixture = FIXTURES["blocks"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_pycozmo(self):
        fixture = FIXTURES["pycozmo"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_chessboard_tl(self):
        fixture = FIXTURES["chessboard_tl"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_chessboard_bl(self):
        fixture = FIXTURES["chessboard_bl"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_chessboard_tr(self):
        fixture = FIXTURES["chessboard_tr"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_chessboard_br(self):
        fixture = FIXTURES["chessboard_br"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_chessboard2_tl(self):
        fixture = FIXTURES["chessboard2_tl"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_chessboard2_bl(self):
        fixture = FIXTURES["chessboard2_bl"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_chessboard2_tr(self):
        fixture = FIXTURES["chessboard2_tr"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)

    def test_chessboard2_br(self):
        fixture = FIXTURES["chessboard2_br"]
        seq = fixture["seq"]
        expected = fixture["image"]
        decoder = self._decode(seq)
        self.assertSameImage(expected, decoder)
