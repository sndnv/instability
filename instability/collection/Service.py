import logging
import os
import time
from multiprocessing.dummy import Pool

from instability.collection.Latency import from_ping
from instability.collection.Speed import from_speedtest
from instability.persistence.SQLite import SQLite


class Service:
    def __init__(self, db, prom, targets, latency_collection_interval, speed_collection_interval):
        """
        Data collection service.

        :param db: SQLite DB file name
        :param prom: Prometheus collector
        :param targets: host to use for collecting latency data
        :param latency_collection_interval: latency data collection interval (in seconds)
        :param speed_collection_interval: network speed data collection interval (in seconds)
        """

        self.db = db
        self.prom = prom
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
        """
        Starts latency data collection and stores it in the configured SQLite database (table must already exist).

        **Note**: `Blocks the current thread indefinitely.`

        :return: `nothing`
        """

        with SQLite(self.db) as store:
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
                        self.prom.latency_add(latency)
                    else:
                        self.log.error("Failed to collect latency data for target [{}]".format(target))

                time.sleep(self.latency_collection_interval)

    def start_speed_collection(self):
        """
        Starts network speed data collection and stores it in the configured SQLite database (table must already exist).

        **Note**: `Blocks the current thread indefinitely.`

        :return: `nothing`
        """

        with SQLite(self.db) as store:
            while True:
                speed = self.pool.apply(from_speedtest)

                if speed:
                    self.log.debug(
                        "Collected speed data for server [{}]: [{}/{}] (down/up)".format(
                            speed.server,
                            speed.download,
                            speed.upload
                        )
                    )
                    store.speed_add(speed)
                    self.prom.speed_add(speed)
                else:
                    self.log.error("Failed to collect speed data")

                time.sleep(self.speed_collection_interval)
