import logging
from datetime import datetime, timedelta
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

        return {
            'targets': latencies.keys(),
            'latencies': json.dumps(latencies, default=str)
        }
