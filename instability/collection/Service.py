import logging
import os
import time
from multiprocessing.dummy import Pool

from instability.collection.Latency import ping
from instability.persistence.SQLite import SQLite


class Service:
    def __init__(self, db, targets, collection_interval):
        self.db = db
        self.targets = targets
        self.collection_interval = collection_interval
        self.pool = Pool(processes=len(os.sched_getaffinity(0)))
        self.log = logging.getLogger("collection-service")

    def start(self):
        with SQLite(self.db) as store:
            if not store.latency_table_exists():
                store.latency_table_create()

            while True:
                latencies = self.pool.map(lambda target: ping(target), self.targets)

                for latency in latencies:
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

                time.sleep(self.collection_interval)
