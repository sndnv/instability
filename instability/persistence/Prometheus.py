from prometheus_client import Gauge, start_http_server


class Prometheus:
    def __init__(self, host, port):
        """
        Prometheus-backed metrics data store.

        :param host:
        :param port:
        """

        self.host = host
        self.port = port
        self.latency = Gauge("latency", "Network latency (ms)", ["target", "type"])
        self.loss = Gauge("loss", "Packet loss (%)", ["target"])
        self.speed = Gauge("speed", "Network speed (bits/s)", ["type"])

    def latency_add(self, latency):
        """
        Adds the supplied latency data to the metrics.

        :param latency: latency data to add
        :return: `nothing`
        """

        if latency.average is not None:
            self.latency.labels(latency.target, "average").set(latency.average)

        if latency.minimum is not None:
            self.latency.labels(latency.target, "minimum").set(latency.minimum)

        if latency.maximum is not None:
            self.latency.labels(latency.target, "maximum").set(latency.maximum)

        if latency.loss is not None:
            self.loss.labels(latency.target).set(latency.loss)

    def speed_add(self, speed):
        """
        Adds the supplied network speed data to the metrics.

        :param speed: speed data to add
        :return: `nothing`
        """

        if speed.download is not None:
            self.speed.labels("download").set(speed.download)

        if speed.upload is not None:
            self.speed.labels("upload").set(speed.upload)

    def start_http_service(self):
        """
        Starts the Prometheus metrics endpoint.

        **Note**: `Non-blocking.`

        :return: `nothing`
        """

        start_http_server(self.port, self.host)
