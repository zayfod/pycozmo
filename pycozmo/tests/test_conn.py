
import unittest
from threading import Event

import pycozmo


class TestConnection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pycozmo.setup_basic_logging(log_level="DEBUG", protocol_log_level="DEBUG")

    def setUp(self):
        self.s_conn_e = Event()
        self.c_conn_e = Event()
        self.s_e = Event()
        self.c_e = Event()
        self.s = pycozmo.conn.Connection(server=True)
        self.s.add_handler(pycozmo.protocol_encoder.Connect, lambda cli, pkt: self.s_conn_e.set())
        self.c = pycozmo.conn.Connection(("127.0.0.1", 5551))
        self.c.add_handler(pycozmo.protocol_encoder.Connect, lambda cli, pkt: self.c_conn_e.set())

    def start(self):
        self.s.start()
        self.c.start()

    def stop(self):
        self.c.stop()
        self.s.stop()

    def connect(self):
        self.c.connect()
        self.assertTrue(self.s_conn_e.wait(2.0))
        self.assertTrue(self.c_conn_e.wait(2.0))

    def disconnect(self):
        self.c.disconnect()

    def test_connect(self):
        self.start()
        self.connect()
        self.disconnect()
        self.stop()

    def test_ping(self):
        self.s.add_handler(pycozmo.protocol_encoder.Ping, lambda cli, pkt: self.s_e.set())
        self.c.add_handler(pycozmo.protocol_encoder.Ping, lambda cli, pkt: self.c_e.set())
        self.start()
        self.connect()
        self.assertTrue(self.c_e.wait(20000.0))
        self.assertTrue(self.s_e.wait(2.0))
        self.stop()

    def test_send_30(self):
        COUNT = 30
        counts = []
        self.s.add_handler(pycozmo.protocol_encoder.SetRobotVolume,
                           lambda cli, pkt: (counts.append(pkt.level), (pkt.level < COUNT - 2) or self.s_e.set()))
        self.start()
        self.connect()
        for i in range(COUNT):
            self.c.send(pycozmo.protocol_encoder.SetRobotVolume(i))
        self.assertTrue(self.s_e.wait(5.0))
        self.assertEqual(counts, list(range(COUNT)))
        self.stop()
