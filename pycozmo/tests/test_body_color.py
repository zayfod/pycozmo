
import struct
import unittest

from pycozmo import protocol_encoder
from pycozmo.protocol_encoder import BodyColor


class TestBodyColor(unittest.TestCase):

    def test_white_v17(self) -> None:
        self.assertEqual(BodyColor(5), BodyColor.WHITE_v17)
        self.assertEqual(BodyColor.WHITE_v17.value, 5)

    def test_body_info_decoding(self) -> None:
        # BodyInfo: serial number (uint32), body HW version (int32), body color (int32).
        data = struct.pack("<Iii", 0x12345678, 7, 5)
        pkt = protocol_encoder.BodyInfo.from_bytes(data)
        self.assertEqual(pkt.body_color, BodyColor.WHITE_v17)
        self.assertEqual(pkt.to_bytes(), data)

    def test_body_info_known_colors(self) -> None:
        for color in (BodyColor.WHITE_v10, BodyColor.WHITE_v15, BodyColor.CE_LM_v15, BodyColor.LE_BL_v16):
            data = struct.pack("<Iii", 1, 5, color.value)
            self.assertEqual(protocol_encoder.BodyInfo.from_bytes(data).body_color, color)
