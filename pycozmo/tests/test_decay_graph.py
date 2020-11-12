
import unittest

from pycozmo.emotions import DecayGraph, Node


class TestDecayGraph(unittest.TestCase):

    def setUp(self):
        self.graph = DecayGraph([
            Node(x=0, y=1),
            Node(x=10, y=1),
            Node(x=60, y=0.6),
            Node(x=100, y=0.2),
        ])

    def test_increment_calculation(self):
        # negative values
        self.assertAlmostEqual(self.graph.get_increment(-1), 1.0)
        # value between nodes
        self.assertAlmostEqual(self.graph.get_increment(40), 0.76)
        # value matches node
        self.assertAlmostEqual(self.graph.get_increment(60), 0.6)
        # value is higher than last node
        self.assertAlmostEqual(self.graph.get_increment(200), -0.8)
