from datetime import datetime

import pingparsing


def from_ping(target, count=10):
    """
    Collects latency data based on `ping`.

    :param target: destination host to ping
    :param count: number of pings to perform (default is 10)
    :return: latency data
    """

    transmitter = pingparsing.PingTransmitter()
    transmitter.destination_host = target
    transmitter.count = count

    parser = pingparsing.PingParsing()

    try:
        raw_result = parser.parse(transmitter.ping())
        result = raw_result.as_dict()

        return Latency(
            target=target,
            loss=result['packet_loss_rate'],
            average=result['rtt_avg'],
            minimum=result['rtt_min'],
            maximum=result['rtt_max']
        )
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return None


class Latency:
    def __init__(self, target, loss, average, minimum, maximum, timestamp=None):
        """
        Latency data container.

        :param target: destination host associated with the data
        :param loss: packet loss rate (as a percentage)
        :param average: average latency (in ms)
        :param minimum: minimum latency (in ms)
        :param maximum: maximum latency (in ms)
        :param timestamp: data collection timestamp
        """
        self._target = target
        self._loss = loss
        self._average = average
        self._minimum = minimum
        self._maximum = maximum
        self._timestamp = timestamp or datetime.utcnow()

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def target(self): return self._target

    @property
    def loss(self): return self._loss

    @property
    def average(self): return self._average

    @property
    def minimum(self): return self._minimum

    @property
    def maximum(self): return self._maximum

    @property
    def timestamp(self): return self._timestamp
