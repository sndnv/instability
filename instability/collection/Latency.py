import pingparsing
from datetime import datetime


def ping(target, count=10):
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination_host = target
    transmitter.count = count

    parser = pingparsing.PingParsing()

    raw_result = transmitter.ping()
    result = parser.parse(raw_result).as_dict()

    return Latency(
        target=target,
        loss=result['packet_loss_rate'],
        average=result['rtt_avg'],
        minimum=result['rtt_min'],
        maximum=result['rtt_max']
    )


class Latency:
    def __init__(self, target, loss, average, minimum, maximum, timestamp=None):
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
