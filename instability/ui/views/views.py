import logging
from datetime import datetime, timedelta, timezone
from itertools import groupby
import json

import iso8601
from pyramid.view import view_config, view_defaults


@view_defaults(renderer='views/index.jinja2')
class IndexView:
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger("index-view")

    @view_config(route_name='index', request_method='GET')
    def index(self):
        store = self.request.registry.store
        start = self.request.params.get("start", None)
        end = self.request.params.get("end", None)

        try:
            start = iso8601.parse_date(start)
        except iso8601.ParseError as e:
            self.log.warning(e)
            start = datetime.utcnow() + timedelta(days=-1)

        try:
            end = iso8601.parse_date(end)
        except iso8601.ParseError as e:
            self.log.warning(e)
            end = datetime.utcnow()

        latencies = store.latency_get_between(start, end)

        def grouping_field(latency): return latency.target

        latencies = dict(
            (k, list(map(lambda e: e.__dict__, g))) for k, g in groupby(sorted(latencies, key=grouping_field), grouping_field)
        )

        for _, latencies_group in latencies.items():
            for latency in latencies_group:
                latency['_timestamp'] = latency['_timestamp'].replace(tzinfo=timezone.utc).astimezone(tz=None)

        speeds = store.speed_get_between(start, end)
        speeds = list(map(lambda e: e.__dict__, speeds))
        for speed in speeds:
            speed['_download'] = round(speed['_download'] / 1000 / 1000, 2)
            speed['_upload'] = round(speed['_upload'] / 1000 / 1000, 2)
            speed['_timestamp'] = speed['_timestamp'].replace(tzinfo=timezone.utc).astimezone(tz=None)

        return {
            'targets': latencies.keys(),
            'latencies': json.dumps(latencies, default=str),
            'speeds': json.dumps(speeds, default=str)
        }
