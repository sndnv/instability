import unittest

from instability.collection.Latency import from_ping, Latency


class LatencySpec(unittest.TestCase):

    def test_should_collect_ping_latency_data(self):
        expected_latency = Latency(
            target="localhost",
            loss=0,
            average=0.0,
            minimum=0.0,
            maximum=0.0
        )

        actual_latency = from_ping(target="localhost", count=4)

        self.assertEqual(expected_latency.loss, actual_latency.loss)
        self.assertLess(expected_latency.average, actual_latency.average)
        self.assertLess(expected_latency.minimum, actual_latency.minimum)
        self.assertLess(expected_latency.maximum, actual_latency.maximum)
