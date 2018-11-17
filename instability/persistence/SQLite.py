import sqlite3

from instability.collection.Latency import Latency
from instability.collection.Speed import Speed


class SQLite:
    def __init__(self, db, check_same_thread=True):
        """
        SQLite-backed data store.

        :param db: SQLite db file name
        """

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
        """
        Checks if the latency table already exists.

        :return: `True` if the latency table exists
        """

        return self.__table_exists(Latency)

    def speed_table_exists(self):
        """
        Checks if the network speed table already exists.

        :return: `True` if the network speed table exists
        """

        return self.__table_exists(Speed)

    def latency_table_size(self):
        """
        Retrieves the number of entries in the latency table.

        :return: number of entries in the latency table
        """

        return self.__table_size(Latency)

    def speed_table_size(self):
        """
        Retrieves the number of entries in the network speed table.

        :return: number of entries in the network speed table
        """

        return self.__table_size(Speed)

    def latency_table_create(self):
        """
        Creates the latency table.

        :return: `nothing`
        """

        self.__table_create(Latency)

    def speed_table_create(self):
        """
        Creates the network speed table.

        :return: `nothing`
        """

        self.__table_create(Speed)

    def latency_add(self, latency):
        """
        Adds the supplied latency data to the DB.

        :param latency: latency data to add
        :return: `nothing`
        """

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

    def speed_add(self, speed):
        """
        Adds the supplied network speed data to the DB.

        :param speed: network speed data to add
        :return: `nothing`
        """

        command = "INSERT INTO speeds VALUES (?, ?, ?, ?)"

        self.db.execute(
            command,
            (
                speed.server,
                speed.download,
                speed.upload,
                speed.timestamp
            )
        )
        self._connection.commit()

    def latency_get(self):
        """
        Retrieves all latency entries.

        :return: all latency entries
        """

        return self.__get(Latency)

    def speed_get(self):
        """
        Retrieves all network speed entries.

        :return: all network speed entries
        """

        return self.__get(Speed)

    def latency_get_between(self, start, end):
        """
        Retrieves all latency entries between the specified timestamps.

        :param start: query start date/time
        :param end: query end date/time
        :return: all latency entries in the specified period
        """

        return self.__get_between(Latency, start, end)

    def speed_get_between(self, start, end):
        """
        Retrieves all network speed entries between the specified timestamps.

        :param start: query start date/time
        :param end: query end date/time
        :return: all network speed entries in the specified period
        """

        return self.__get_between(Speed, start, end)

    def __table_exists(self, collection_data_type):
        table = self.__collection_data_to_table(collection_data_type)
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table)
        self.db.execute(query)
        exists = len(self.db.fetchone() or []) != 0
        return exists

    def __table_size(self, collection_data_type):
        table = self.__collection_data_to_table(collection_data_type)
        query = "SELECT count(*) FROM {}".format(table)
        self.db.execute(query)
        count = self.db.fetchone()[0]
        return count

    def __table_create(self, collection_data_type):
        table = self.__collection_data_to_table(collection_data_type)
        table_fields = self.__collection_data_to_table_field_definitions(collection_data_type)
        command = "CREATE TABLE {} ({})".format(table, table_fields)

        self.db.execute(command)
        self._connection.commit()

    def __get(self, collection_data_type):
        table = self.__collection_data_to_table(collection_data_type)
        table_fields = self.__collection_data_to_table_fields(collection_data_type)
        query = "SELECT {} FROM {}".format(table_fields, table)

        self.db.execute(query)
        collection_data = list(map(self.__row_to_collection_data(collection_data_type), self.db.fetchall()))

        return collection_data

    def __get_between(self, collection_data_type, start, end):
        table = self.__collection_data_to_table(collection_data_type)
        table_fields = self.__collection_data_to_table_fields(collection_data_type)
        query = "SELECT {} FROM {} WHERE timestamp BETWEEN ? AND ?".format(table_fields, table)

        self.db.execute(query, (start, end))
        speeds = list(map(self.__row_to_collection_data(collection_data_type), self.db.fetchall()))

        return speeds

    @staticmethod
    def __collection_data_to_table(collection_data_type):
        return {
            Latency: "latencies",
            Speed: "speeds"
        }.get(collection_data_type, None)

    @staticmethod
    def __collection_data_to_table_field_definitions(collection_data_type):
        return {
            Latency: "target text, loss double, average double, minimum double, maximum double, timestamp timestamp",
            Speed: "server text, download double, upload double, timestamp timestamp"
        }.get(collection_data_type, None)

    @staticmethod
    def __collection_data_to_table_fields(collection_data_type):
        return {
            Latency: "target, loss, average, minimum, maximum, timestamp",
            Speed: "server, download, upload, timestamp"
        }.get(collection_data_type, None)

    @staticmethod
    def __row_to_collection_data(collection_data_type):
        return {
            Latency: lambda row: Latency(
                target=row[0],
                loss=row[1],
                average=row[2],
                minimum=row[3],
                maximum=row[4],
                timestamp=row[5]
            ),
            Speed: lambda row: Speed(
                server=row[0],
                download=row[1],
                upload=row[2],
                timestamp=row[3]
            )
        }.get(collection_data_type, None)
