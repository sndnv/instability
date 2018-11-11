import os
import unittest
from datetime import datetime, timedelta

from instability.collection.Latency import Latency
from instability.persistence.SQLite import SQLite


class SQLiteSpec(unittest.TestCase):

    def setUp(self):
        self.db_file = "test.db"

    def tearDown(self):
        os.remove(self.db_file)

    def test_should_create_latency_table(self):
        with SQLite(db=self.db_file) as store:
            self.assertFalse(store.latency_table_exists())
            store.latency_table_create()
            self.assertTrue(store.latency_table_exists())

    def test_should_add_latencies(self):
        with SQLite(db=self.db_file) as store:
            latency = Latency(
                target="localhost",
                loss=0,
                average=0.0,
                minimum=0.0,
                maximum=0.0
            )

            store.latency_table_create()
            self.assertEqual(store.latency_table_size(), 0)

            store.latency_add(latency)
            self.assertEqual(store.latency_table_size(), 1)

            store.latency_add(latency)
            self.assertEqual(store.latency_table_size(), 2)

            store.latency_add(latency)
            store.latency_add(latency)
            self.assertEqual(store.latency_table_size(), 4)

    def test_should_query_latencies(self):
        with SQLite(db=self.db_file) as store:
            latency_1 = Latency(
                target="localhost",
                loss=0,
                average=0.0,
                minimum=0.0,
                maximum=0.0
            )

            latency_2 = Latency(
                target="localhost",
                loss=0.75,
                average=1.0,
                minimum=2.0,
                maximum=3.0
            )

            latency_3 = Latency(
                target="example.com",
                loss=0,
                average=0.0,
                minimum=0.0,
                maximum=0.0
            )

            store.latency_table_create()
            store.latency_add(latency_1)
            store.latency_add(latency_2)
            store.latency_add(latency_3)

            expected_list = [latency_1, latency_2, latency_3]
            actual_list = store.latency_get()

            self.assertListEqual(expected_list, actual_list)

    def test_should_query_latency_in_interval(self):
        with SQLite(db=self.db_file) as store:
            latency_1 = Latency(
                target="localhost",
                loss=0,
                average=0.0,
                minimum=0.0,
                maximum=0.0,
                timestamp=datetime.utcnow() + timedelta(days=-3)
            )

            latency_2 = Latency(
                target="localhost",
                loss=0.75,
                average=1.0,
                minimum=2.0,
                maximum=3.0,
                timestamp=datetime.utcnow() + timedelta(days=2)
            )

            latency_3 = Latency(
                target="example.com",
                loss=0,
                average=0.0,
                minimum=0.0,
                maximum=0.0,
                timestamp=datetime.utcnow() + timedelta(days=-5)
            )

            store.latency_table_create()
            store.latency_add(latency_1)
            store.latency_add(latency_2)
            store.latency_add(latency_3)

            expected_list = [latency_1, latency_3]
            actual_list = store.latency_get_between(
                start=datetime.utcnow() + timedelta(days=-10),
                end=datetime.utcnow() + timedelta(days=1)
            )

            self.assertListEqual(expected_list, actual_list)
