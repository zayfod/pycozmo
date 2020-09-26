
import unittest
import logging

from pycozmo.robot_debug import get_log_level, get_debug_message


class TestLogLevel(unittest.TestCase):

    def test_invalid(self):
        level = get_log_level(-1)
        self.assertEqual(level, logging.DEBUG)

    def test_debug(self):
        level = get_log_level(1)
        self.assertEqual(level, logging.DEBUG)

    def test_debug2(self):
        level = get_log_level(2)
        self.assertEqual(level, logging.DEBUG)

    def test_info(self):
        level = get_log_level(3)
        self.assertEqual(level, logging.INFO)

    def test_warning(self):
        level = get_log_level(4)
        self.assertEqual(level, logging.WARNING)

    def test_error(self):
        level = get_log_level(5)
        self.assertEqual(level, logging.ERROR)


class TestDebugMessage(unittest.TestCase):

    def test_no_name_no_format(self):
        msg = get_debug_message(-1, -1, [])
        self.assertEqual(msg, "")

    def test_no_format(self):
        msg = get_debug_message(0, -1, [])
        self.assertEqual(msg, "ASSERT")

    def test_no_name(self):
        msg = get_debug_message(-1, 0, [])
        self.assertEqual(msg, "Invalid format ID")

    def test_name_format(self):
        msg = get_debug_message(7, 3, [])
        self.assertEqual(msg, "HeadController: Initializing")

    def test_name_format_args(self):
        msg = get_debug_message(409, 624, [0, 0x11, 0x22, 0x33, 0x44, 0x55])
        self.assertEqual(msg, "macaddr.soft_ap: 00:11:22:33:44:55")

    def test_name_format_invalid_args(self):
        with self.assertRaises(AssertionError):
            get_debug_message(409, 624, [])
