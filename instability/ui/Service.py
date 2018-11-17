from pyramid.config import Configurator
from waitress import serve

from instability.persistence.SQLite import SQLite


class Service:
    def __init__(self, db, host, port):
        """
        Web service.

        :param db: SQLite db file name
        :param host: hostname to bind the web service to
        :param port: port to bind the web service to
        """

        self.db = db
        self.host = host
        self.port = port

    def start(self):
        """
        Starts the web service on the configured interface/hostname and port.

        **Note**: `Blocks the current thread indefinitely.`

        :return: `nothing`
        """

        with SQLite(db=self.db, check_same_thread=False) as store:
            with Configurator() as config:
                config.include('pyramid_jinja2')
                config.registry.store = store
                config.add_route('index', '/')
                config.scan('.views.views')
                config.add_static_view('static', 'static', cache_max_age=3600)
                app = config.make_wsgi_app()

            serve(app, host=self.host, port=self.port)
