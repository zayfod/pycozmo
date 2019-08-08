
import unittest

from pycozmo.window import BaseWindow, ReceiveWindow, SendWindow


class TestBaseWindowCreate(unittest.TestCase):

    def test_create(self):
        w = BaseWindow(4)
        self.assertEqual(w.size, 8)
        self.assertEqual(w.expected_seq, 1)
        self.assertEqual(w.last_seq, 0)
        self.assertEqual(w.max_seq, 16)

    def test_create_limted(self):
        w = ReceiveWindow(4, size=5)
        self.assertEqual(w.size, 5)
        self.assertEqual(w.expected_seq, 1)
        self.assertEqual(w.last_seq, 0)
        self.assertEqual(w.max_seq, 16)

    def test_create_invalid(self):
        with self.assertRaises(ValueError):
            ReceiveWindow(3, size=10)


class TestBaseWindow(unittest.TestCase):

    def setUp(self):
        self.w = BaseWindow(4)

    def test_is_valid_seq_negative(self):
        self.assertFalse(self.w.is_valid_seq(-1))

    def test_is_valid_seq_too_large(self):
        self.assertFalse(self.w.is_valid_seq(16))

    def test_is_valid_seq(self):
        self.assertTrue(self.w.is_valid_seq(0))


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
        self.assertTrue(self.w.is_out_of_order(15))
        self.assertTrue(self.w.is_out_of_order(16))

    def test_is_out_of_order_one(self):
        self.w.put("1")
        self.assertTrue(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(1))
        self.assertTrue(self.w.is_out_of_order(2))
        self.assertTrue(self.w.is_out_of_order(16))

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
