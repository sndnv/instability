import sqlite3
from instability.collection.Latency import Latency


class SQLite:
    def __init__(self, db, check_same_thread=True):
        self._connection = sqlite3.connect(
            db,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            check_same_thread=check_same_thread
        )

        self.db = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._connection.close()

    def latency_table_exists(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='latencies'"
        self.db.execute(query)
        exists = len(self.db.fetchone() or []) != 0
        return exists

    def latency_table_size(self):
        query = "SELECT count(*) FROM latencies"
        self.db.execute(query)
        count = self.db.fetchone()[0]
        return count

    def latency_table_create(self):
        command = (
            "CREATE TABLE latencies ("
            "target text,"
            "loss double,"
            "average double,"
            "minimum double,"
            "maximum double,"
            "timestamp timestamp"
            ")"
        )

        self.db.execute(command)
        self._connection.commit()

    def latency_add(self, latency):
        command = "INSERT INTO latencies VALUES (?, ?, ?, ?, ?, ?)"

        self.db.execute(
            command,
            (
                latency.target,
                latency.loss,
                latency.average,
                latency.minimum,
                latency.maximum,
                latency.timestamp
            )
        )
        self._connection.commit()

    def latency_get(self):
        query = (
            "SELECT target, loss, average, minimum, maximum, timestamp FROM latencies"
        )

        self.db.execute(query)
        latencies = list(
            map(
                lambda row: Latency(
                    target=row[0],
                    loss=row[1],
                    average=row[2],
                    minimum=row[3],
                    maximum=row[4],
                    timestamp=row[5]
                ),
                self.db.fetchall()
            )
        )

        return latencies

    def latency_get_between(self, start, end):
        query = (
            "SELECT target, loss, average, minimum, maximum, timestamp FROM latencies "
            "WHERE timestamp BETWEEN ? AND ?"
        )
        self.db.execute(query, (start, end))
        latencies = list(
            map(
                lambda row: Latency(
                    target=row[0],
                    loss=row[1],
                    average=row[2],
                    minimum=row[3],
                    maximum=row[4],
                    timestamp=row[5]
                ),
                self.db.fetchall()
            )
        )

        return latencies
