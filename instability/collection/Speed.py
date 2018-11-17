from datetime import datetime

from speedtest import Speedtest


def from_speedtest():
    """
    Collects network speed data based on `speedtest.net`.

    :return: network speed data
    """

    try:
        speedtest = Speedtest()
        speedtest.get_best_server()
        speedtest.download()
        speedtest.upload()

        return Speed(
            download=speedtest.results.download,
            upload=speedtest.results.upload,
            server=speedtest.results.server['host']
        )
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return None


class Speed:
    def __init__(self, download, upload, server, timestamp=None):
        """
        Network speed data container.

        :param download: download speed (bits/s)
        :param upload:  upload speed (bits/s)
        :param server: test server
        :param timestamp: data collection timestamp
        """

        self._download = download
        self._upload = upload
        self._server = server
        self._timestamp = timestamp or datetime.utcnow()

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def download(self): return self._download

    @property
    def upload(self): return self._upload

    @property
    def server(self): return self._server

    @property
    def timestamp(self): return self._timestamp
