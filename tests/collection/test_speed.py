import unittest

from instability.collection.Speed import from_speedtest, Speed


class SpeedSpec(unittest.TestCase):

    def test_should_collect_speedtest_speed_data(self):
        expected_speed = Speed(
            download=0,
            upload=0,
            server=None
        )

        actual_speed = from_speedtest()

        self.assertLess(expected_speed.download, actual_speed.download)
        self.assertLess(expected_speed.upload, actual_speed.upload)
