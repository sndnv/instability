import unittest

from instability.collection.Speed import Speed
from prometheus_client import REGISTRY

from instability.collection.Latency import Latency
from instability.persistence.Prometheus import Prometheus


class PrometheusSpec(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.registry = REGISTRY
        cls.store = Prometheus(host="localhost", port="9999")

    def test_should_add_latencies(self):

        self.assertEqual(None, self.registry.get_sample_value("latency", {"target": "localhost", "type": "average"}))
        self.assertEqual(None, self.registry.get_sample_value("latency", {"target": "localhost", "type": "minimum"}))
        self.assertEqual(None, self.registry.get_sample_value("latency", {"target": "localhost", "type": "maximum"}))
        self.assertEqual(None, self.registry.get_sample_value("latency", {"target": "192.168.1.1", "type": "average"}))
        self.assertEqual(None, self.registry.get_sample_value("latency", {"target": "192.168.1.1", "type": "minimum"}))
        self.assertEqual(None, self.registry.get_sample_value("latency", {"target": "192.168.1.1", "type": "maximum"}))

        self.assertEqual(None, self.registry.get_sample_value("loss", {"target": "localhost"}))
        self.assertEqual(None, self.registry.get_sample_value("loss", {"target": "192.168.1.1"}))

        latency_1 = Latency(
            target="localhost",
            loss=1,
            average=2.0,
            minimum=3.0,
            maximum=4.0
        )

        latency_2 = Latency(
            target="192.168.1.1",
            loss=5,
            average=10.0,
            minimum=15.0,
            maximum=20.0
        )

        self.store.latency_add(latency_1)
        self.store.latency_add(latency_2)

        self.assertEqual(2, self.registry.get_sample_value("latency", {"target": "localhost", "type": "average"}))
        self.assertEqual(3, self.registry.get_sample_value("latency", {"target": "localhost", "type": "minimum"}))
        self.assertEqual(4, self.registry.get_sample_value("latency", {"target": "localhost", "type": "maximum"}))
        self.assertEqual(10, self.registry.get_sample_value("latency", {"target": "192.168.1.1", "type": "average"}))
        self.assertEqual(15, self.registry.get_sample_value("latency", {"target": "192.168.1.1", "type": "minimum"}))
        self.assertEqual(20, self.registry.get_sample_value("latency", {"target": "192.168.1.1", "type": "maximum"}))

        self.assertEqual(1, self.registry.get_sample_value("loss", {"target": "localhost"}))
        self.assertEqual(5, self.registry.get_sample_value("loss", {"target": "192.168.1.1"}))

    def test_should_add_speed(self):

        self.assertEqual(None, self.registry.get_sample_value("speed", {"type": "download"}))
        self.assertEqual(None, self.registry.get_sample_value("speed", {"type": "upload"}))
        self.assertEqual(None, self.registry.get_sample_value("speed", {"type": "download"}))
        self.assertEqual(None, self.registry.get_sample_value("speed", {"type": "upload"}))

        speed = Speed(
            server="test-server-1",
            download=1,
            upload=2
        )

        self.store.speed_add(speed)

        self.assertEqual(1, self.registry.get_sample_value("speed", {"type": "download"}))
        self.assertEqual(2, self.registry.get_sample_value("speed", {"type": "upload"}))
