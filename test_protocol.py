
import unittest
import random

from protocol import Frame, BaseWindow, ReceiveWindow, ReceiveThread, SendWindow


class TestFrame(unittest.TestCase):

    def test_from_bytes_multi(self):
        f = Frame()
        f.from_bytes(
            b'COZ\x03RE\x01\x07\x9d\n\xa0\n\x8f\x00\x04\x01\x00\x8f\x04\x1d\x00\x97\x1a\x00\x15\xb0\xaa\x9c'
            b'\xac\xb2@\xa8\xba^\xac\xb2@\x02\xb4\xa2\xa0\xb0\xaa@\xac\xb2`\xb0\xaa\x1b\x04 \x00\x03\x1f\x80'
            b'\x1f\x80\t\x00\x00\x00\x00\x00\x1f\x80\x1f\x80\t\x00\x00\x00\x00\x00\x1f\x80\x1f\x80\t\x00\x00'
            b'\x00\x00\x00\x00\x04\x16\x00\x11\x1f\x80\x1f\x80\t\x00\x00\x00\x00\x00\x1f\x80\x1f\x80\t\x00'
            b'\x00\x00\x00\x00\x00')
        self.assertEqual(f.type, 7)
        self.assertEqual(f.first_seq, 2717)
        self.assertEqual(f.seq, 2720)
        self.assertEqual(f.ack, 143)
        self.assertEqual(len(f.pkts), 4)


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
        self.assertTrue(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(1))
        self.assertTrue(self.w.is_out_of_order(10))

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


class TestReceiveThread(unittest.TestCase):

    def setUp(self):
        # noinspection PyTypeChecker
        self.p = ReceiveThread(None, None, seq_bits=4, window_size=2)
        self.p.deliver = lambda data: self.output.append(data)
        self.output = []

    def test_handle_pkt(self):
        self.p.handle_pkt(1, "1")
        self.p.handle_pkt(2, "2")
        self.p.handle_pkt(3, "3")
        self.assertEqual(self.output, ["1", "2", "3"])

    def test_handle_pkt_duplicates(self):
        self.p.handle_pkt(1, "1")
        self.p.handle_pkt(1, "1")
        self.p.handle_pkt(2, "2")
        self.p.handle_pkt(2, "2")
        self.p.handle_pkt(3, "3")
        self.p.handle_pkt(3, "3")
        self.p.handle_pkt(4, "4")
        self.p.handle_pkt(4, "4")
        self.p.handle_pkt(5, "5")
        self.p.handle_pkt(5, "5")
        self.p.handle_pkt(5, "5")
        self.p.handle_pkt(6, "6")
        self.p.handle_pkt(6, "6")
        self.p.handle_pkt(6, "6")
        self.assertEqual(self.output, ["1", "2", "3", "4", "5", "6"])

    def test_handle_pkt_order(self):
        self.p.handle_pkt(2, "2")
        self.p.handle_pkt(1, "1")
        self.p.handle_pkt(3, "3")
        self.p.handle_pkt(4, "4")
        self.p.handle_pkt(6, "6")
        self.p.handle_pkt(5, "5")
        self.assertEqual(self.output, ["1", "2", "3", "4", "5", "6"])


class TestReceiveThreadLong(unittest.TestCase):

    def setUp(self):
        # noinspection PyTypeChecker
        self.p = ReceiveThread(None, None, seq_bits=4, window_size=None)
        self.p.deliver = lambda data: self.output.append(data)
        self.output = []

    def test_handle_pkt_long(self):
        num_pkts = 16 * 1024
        for i in range(1, num_pkts + 1):
            self.p.handle_pkt(i % 16, i)
        self.assertEqual(self.output, list(range(1, num_pkts + 1)))

    def test_handle_pkt_long_order(self):
        num_pkts = 16 * 1024
        for i in range(1, num_pkts + 1, 16):
            for j in range(i, i + 16, 8):
                sequence = list(range(j, j + 8))
                random.shuffle(sequence)
                for k in sequence:
                    self.p.handle_pkt(k % 16, k)
        self.assertEqual(self.output, list(range(1, num_pkts + 1)))


class TestTransmitWindow(unittest.TestCase):

    def setUp(self):
        self.w = SendWindow(4)

    def test_is_out_of_order_empty(self):
        self.assertTrue(self.w.is_out_of_order(0))
        self.assertTrue(self.w.is_out_of_order(1))
        self.assertTrue(self.w.is_out_of_order(15))
        self.assertTrue(self.w.is_out_of_order(16))

    def test_is_out_of_order_one(self):
        self.w.put(0.0, "1")
        self.assertTrue(self.w.is_out_of_order(0))
        self.assertFalse(self.w.is_out_of_order(1))
        self.assertTrue(self.w.is_out_of_order(2))
        self.assertTrue(self.w.is_out_of_order(16))

    def test_is_empty(self):
        self.assertTrue(self.w.is_empty())
        self.w.put(0.0, "0")
        self.assertFalse(self.w.is_empty())
        self.w.pop()
        self.assertTrue(self.w.is_empty())

    def test_is_full(self):
        for i in range(8):
            self.assertFalse(self.w.is_full())
            self.w.put(0.0, str(i))
        self.assertTrue(self.w.is_full())
        for _ in range(8):
            self.w.pop()
            self.assertFalse(self.w.is_full())
