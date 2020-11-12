
import unittest

from pycozmo.window import BaseWindow, ReceiveWindow, SendWindow
from pycozmo.exception import NoSpace


class TestBaseWindowCreate(unittest.TestCase):

    def test_create_1(self):
        w = BaseWindow(1)
        self.assertEqual(w.size, 1)
        self.assertEqual(w.expected_seq, 0)
        self.assertEqual(w.max_seq, 2)

    def test_create_4(self):
        w = BaseWindow(4)
        self.assertEqual(w.size, 8)
        self.assertEqual(w.expected_seq, 0)
        self.assertEqual(w.max_seq, 16)

    def test_create_4_limited(self):
        w = BaseWindow(4, size=8)
        self.assertEqual(w.size, 8)
        self.assertEqual(w.expected_seq, 0)
        self.assertEqual(w.max_seq, 16)

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
        self.w = ReceiveWindow(3, size=4)

    def test_is_out_of_order(self):
        self.assertFalse(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(3))
        self.assertTrue(self.w.is_out_of_order(4))
        self.assertTrue(self.w.is_out_of_order(7))

    def test_is_out_of_order_wrapped(self):
        self.w.expected_seq = 7
        self.w.last_seq = (self.w.expected_seq + self.w.size - 1) % self.w.max_seq
        self.assertTrue(self.w.is_out_of_order(6))
        self.assertFalse(self.w.is_out_of_order(7))
        self.assertFalse(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(1))
        self.assertFalse(self.w.is_out_of_order(2))
        self.assertTrue(self.w.is_out_of_order(3))

    def test_exists(self):
        self.assertFalse(self.w.exists(0))
        self.assertFalse(self.w.exists(1))
        self.w.put(1, "1")
        self.assertFalse(self.w.exists(0))
        self.assertTrue(self.w.exists(1))

    def test_put_get(self):
        self.assertIsNone(self.w.get())
        self.w.put(1, "1")
        self.w.put(0, "0")
        self.assertEqual(self.w.get(), "0")
        self.assertEqual(self.w.get(), "1")
        self.assertIsNone(self.w.get())

    def test_sequence(self):
        sequence = list(range(1, 100))
        expected_sequence = list(range(1, 100))
        received_sequence = []
        for seq, data in enumerate(sequence):
            self.w.put(seq % self.w.max_seq, data)
            data = self.w.get()
            if data:
                received_sequence.append(data)
        self.assertEqual(received_sequence, expected_sequence)

    def test_sequence2(self):
        sequence = [
            (0, 1),
            (1, 2),
            (2, 3),
            (4, 5),
            (3, 4),
            (5, 6),
            (7, 8),
            (6, 7),
            (0, 9),
            (1, 10),
        ]
        expected_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        received_sequence = []
        for seq, data in sequence:
            self.w.put(seq, data)
            while True:
                data = self.w.get()
                if data:
                    received_sequence.append(data)
                else:
                    break
        self.assertEqual(expected_sequence, received_sequence)


class TestSendWindow(unittest.TestCase):

    def setUp(self):
        self.w = SendWindow(3, size=4)

    def test_is_out_of_order_empty(self):
        for i in range(-2, self.w.max_seq + 2):
            self.assertTrue(self.w.is_out_of_order(i))

    def test_is_out_of_order_full(self):
        self.w.put("x")
        self.w.put("y")
        self.w.put("z")
        self.assertTrue(self.w.is_out_of_order(7))
        self.assertFalse(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(1))
        self.assertFalse(self.w.is_out_of_order(2))
        self.assertTrue(self.w.is_out_of_order(3))

    def test_is_out_of_order_full_wrapped(self):
        self.w.expected_seq = 6
        self.w.next_seq = 6
        self.w.put("w")
        self.w.put("x")
        self.w.put("y")
        self.w.put("z")
        self.assertFalse(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(1))
        self.assertTrue(self.w.is_out_of_order(2))
        self.assertTrue(self.w.is_out_of_order(5))
        self.assertFalse(self.w.is_out_of_order(6))
        self.assertFalse(self.w.is_out_of_order(7))

    def test_is_out_of_order_one(self):
        self.w.put("1")
        self.assertTrue(self.w.is_out_of_order(7))
        self.assertFalse(self.w.is_out_of_order(0))
        self.assertTrue(self.w.is_out_of_order(1))

    def test_is_full(self):
        self.assertFalse(self.w.is_full())
        self.w.put("w")
        self.assertFalse(self.w.is_full())
        self.w.put("x")
        self.assertFalse(self.w.is_full())
        self.w.put("y")
        self.assertFalse(self.w.is_full())
        self.w.put("z")
        self.assertTrue(self.w.is_full())

    def test_is_full_wrapped(self):
        self.w.expected_seq = 6
        self.w.next_seq = 6
        self.assertFalse(self.w.is_full())
        self.w.put("w")
        self.assertFalse(self.w.is_full())
        self.w.put("x")
        self.assertFalse(self.w.is_full())
        self.w.put("y")
        self.assertFalse(self.w.is_full())
        self.w.put("z")
        self.assertTrue(self.w.is_full())

    def test_put(self):
        self.assertEqual(self.w.window, [None, None, None, None])
        self.w.put("x")
        self.assertEqual(self.w.expected_seq, 0)
        self.assertEqual(self.w.next_seq, 1)
        self.assertEqual(self.w.window, ["x", None, None, None])

    def test_put_full(self):
        self.w.put("w")
        self.w.put("x")
        self.w.put("y")
        self.w.put("z")
        self.assertEqual(self.w.expected_seq, 0)
        self.assertEqual(self.w.next_seq, 4)
        self.assertEqual(self.w.window, ["w", "x", "y", "z"])

    def test_put_full_exception(self):
        self.w.put("w")
        self.w.put("x")
        self.w.put("y")
        self.w.put("z")
        with self.assertRaises(NoSpace):
            self.w.put("e")

    def test_acknowledge_empty(self):
        self.w.acknowledge(5)
        self.assertEqual(self.w.window, [None, None, None, None])
        self.assertEqual(self.w.expected_seq, 0)
        self.assertEqual(self.w.next_seq, 0)

    def test_acknowledge(self):
        self.w.put("x")
        self.w.put("y")
        self.w.put("z")
        self.w.acknowledge(1)
        self.assertEqual(self.w.window, [None, None, "z", None])
        self.assertEqual(self.w.expected_seq, 2)
        self.assertEqual(self.w.next_seq, 3)

    def test_acknowledge_wrapped(self):
        self.w.expected_seq = 6
        self.w.next_seq = 6
        self.w.put("x")
        self.w.put("y")
        self.w.put("z")
        self.w.acknowledge(7)
        self.assertEqual(self.w.window, ["z", None, None, None])
        self.assertEqual(self.w.expected_seq, 0)
        self.assertEqual(self.w.next_seq, 1)

    def test_get_empty(self):
        self.assertEqual(self.w.get(), [])

    def test_get(self):
        self.w.put("x")
        self.w.put("y")
        self.w.put("z")
        self.assertEqual(self.w.get(), [(0, "x"), (1, "y"), (2, "z")])

    def test_get_wrapped(self):
        self.w.expected_seq = 6
        self.w.next_seq = 6
        self.w.put("x")
        self.w.put("y")
        self.w.put("z")
        self.assertEqual(self.w.get(), [(6, "x"), (7, "y"), (0, "z")])
