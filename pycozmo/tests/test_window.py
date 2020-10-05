
import unittest

from pycozmo.window import BaseWindow, ReceiveWindow, SendWindow


class TestBaseWindowCreate(unittest.TestCase):

    def test_create_1(self):
        w = BaseWindow(1)
        self.assertEqual(w.size, 1)
        self.assertEqual(w.expected_seq, 1)
        self.assertEqual(w.last_seq, 0)
        self.assertEqual(w.max_seq, 1)

    def test_create_4(self):
        w = BaseWindow(4)
        self.assertEqual(w.size, 8)
        self.assertEqual(w.expected_seq, 1)
        self.assertEqual(w.last_seq, 0)
        self.assertEqual(w.max_seq, 15)

    def test_create_4_limited(self):
        w = BaseWindow(4, size=5)
        self.assertEqual(w.size, 5)
        self.assertEqual(w.expected_seq, 1)
        self.assertEqual(w.last_seq, 0)
        self.assertEqual(w.max_seq, 15)

    def test_create_invalid(self):
        with self.assertRaises(ValueError):
            BaseWindow(-1)

    def test_create_invalid2(self):
        with self.assertRaises(ValueError):
            BaseWindow(0)

    def test_create_limited_invalid(self):
        with self.assertRaises(ValueError):
            BaseWindow(3, size=0)

    def test_create_limited_invalid2(self):
        with self.assertRaises(ValueError):
            BaseWindow(3, size=10)


class TestBaseWindowIsValidSeq1(unittest.TestCase):

    def setUp(self):
        self.w = BaseWindow(1)

    def test_negative(self):
        self.assertFalse(self.w.is_valid_seq(-1))

    def test_first_valid(self):
        self.assertTrue(self.w.is_valid_seq(0))

    def test_last_valid(self):
        self.assertTrue(self.w.is_valid_seq(1))

    def test_too_large(self):
        self.assertFalse(self.w.is_valid_seq(2))

    def test_too_large2(self):
        self.assertFalse(self.w.is_valid_seq(100))


class TestBaseWindowIsValidSeq4(unittest.TestCase):

    def setUp(self):
        self.w = BaseWindow(4)

    def test_negative(self):
        self.assertFalse(self.w.is_valid_seq(-1))

    def test_first_valid(self):
        self.assertTrue(self.w.is_valid_seq(0))

    def test_last_valid(self):
        self.assertTrue(self.w.is_valid_seq(15))

    def test_too_large(self):
        self.assertFalse(self.w.is_valid_seq(16))

    def test_too_large2(self):
        self.assertFalse(self.w.is_valid_seq(100))


class TestBaseWindowIsValidSeq16(unittest.TestCase):

    def setUp(self):
        self.w = BaseWindow(16)

    def test_negative(self):
        self.assertFalse(self.w.is_valid_seq(-1))

    def test_first_valid(self):
        self.assertTrue(self.w.is_valid_seq(0))

    def test_last_valid(self):
        self.assertTrue(self.w.is_valid_seq(65535))

    def test_too_large(self):
        self.assertFalse(self.w.is_valid_seq(65536))

    def test_too_large2(self):
        self.assertFalse(self.w.is_valid_seq(100000))


class TestReceiveWindow(unittest.TestCase):

    def setUp(self):
        self.w = ReceiveWindow(4)

    def test_is_out_of_order(self):
        self.assertFalse(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(1))
        self.assertFalse(self.w.is_out_of_order(10))

    def test_exists(self):
        self.assertFalse(self.w.exists(0))
        self.assertFalse(self.w.exists(1))
        self.w.put(1, "1")
        self.assertFalse(self.w.exists(0))
        self.assertTrue(self.w.exists(1))

    def test_is_expected(self):
        self.assertTrue(self.w.is_expected(1))
        self.assertFalse(self.w.is_expected(2))

    def test_get(self):
        self.assertIsNone(self.w.get())
        self.w.put(2, "2")
        self.w.put(1, "1")
        self.assertEqual(self.w.get(), "1")
        self.assertEqual(self.w.get(), "2")
        self.assertIsNone(self.w.get())


class TestTransmitWindow(unittest.TestCase):

    def setUp(self):
        self.w = SendWindow(4)

    def test_is_out_of_order_empty(self):
        self.assertTrue(self.w.is_out_of_order(0))
        self.assertTrue(self.w.is_out_of_order(1))
        self.assertTrue(self.w.is_out_of_order(14))
        self.assertTrue(self.w.is_out_of_order(15))

    def test_is_out_of_order_one(self):
        self.w.put("1")
        self.assertTrue(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(1))
        self.assertTrue(self.w.is_out_of_order(2))
        self.assertTrue(self.w.is_out_of_order(15))

    def test_is_empty(self):
        self.assertTrue(self.w.is_empty())
        self.w.put("0")
        self.assertFalse(self.w.is_empty())
        self.w.pop()
        self.assertTrue(self.w.is_empty())

    def test_is_full(self):
        for i in range(8):
            self.assertFalse(self.w.is_full())
            self.w.put(str(i))
        self.assertTrue(self.w.is_full())
        for _ in range(8):
            self.w.pop()
            self.assertFalse(self.w.is_full())
