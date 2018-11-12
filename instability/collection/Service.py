import logging
import os
import time
from multiprocessing.dummy import Pool

from instability.collection.Latency import from_ping
from instability.collection.Speed import from_speedtest
from instability.persistence.SQLite import SQLite


class Service:
    def __init__(self, db, targets, latency_collection_interval, speed_collection_interval):
        self.db = db
        self.targets = targets
        self.latency_collection_interval = latency_collection_interval
        self.speed_collection_interval = speed_collection_interval
        self.pool = Pool(processes=len(os.sched_getaffinity(0)))
        self.log = logging.getLogger("collection-service")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pool.close()
        self.pool.terminate()

    def start_latency_collection(self):
        with SQLite(self.db) as store:
            if not store.latency_table_exists():
                store.latency_table_create()

            while True:
                latencies = self.pool.map(lambda target: (target, from_ping(target)), self.targets)

                for target, latency in latencies:
                    if latency:
                        self.log.debug(
                            "Collected latency data for target [{}]: [{}/{} ({}) | {}] (min/max (avg) | loss)".format(
                                latency.target,
                                latency.minimum,
                                latency.maximum,
                                latency.average,
                                latency.loss
                            )
                        )
                        store.latency_add(latency)
                    else:
                        self.log.error("Failed to collect latency data for target [{}]".format(target))

                time.sleep(self.latency_collection_interval)

    def start_speed_collection(self):
        with SQLite(self.db) as store:
            if not store.speed_table_exists():
                store.speed_table_create()

            while True:
                speed = self.pool.apply(from_speedtest)

                self.log.debug(
                    "Collected speed data for server [{}]: [{}/{}] (down/up)".format(
                        speed.server,
                        speed.download,
                        speed.upload
                    )
                )
                store.speed_add(speed)

                time.sleep(self.speed_collection_interval)
