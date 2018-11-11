from pyramid.config import Configurator
from waitress import serve

from instability.persistence.SQLite import SQLite


class Service:
    def __init__(self, db, host, port):
        self.db = db
        self.host = host
        self.port = port

    def start(self):
        with SQLite(db=self.db, check_same_thread=False) as store:
            with Configurator() as config:
                config.include('pyramid_jinja2')
                config.registry.store = store
                config.add_route('index', '/')
                config.scan('.views.views')
                config.add_static_view('static', 'static', cache_max_age=3600)
                app = config.make_wsgi_app()

            serve(app, host=self.host, port=self.port)
