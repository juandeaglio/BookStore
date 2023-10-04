import os
import unittest
from Source.WebServer import WebServer
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy
from Source.WebServerStrategy.GunicornNginxStrategy import GunicornNginxStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy
from test.FakedProcessLibrary import FakedProcessLibrary
from test.FakedOSLibrary import FakedOSLibrary


class TestDjangoWebServer(unittest.TestCase):
    def test_startServer(self, strategy=DjangoStrategy, osLibrary=FakedOSLibrary(os.name)):
        self.webserver = WebServer(strategy=strategy,
                                   processLibrary=FakedProcessLibrary,
                                   osLibrary=osLibrary)
        self.webserver.start()
        assert self.webserver.process is not None

    def test_startAndStopServer(self, strategy=DjangoStrategy, osLibrary=FakedOSLibrary(os.name)):
        self.webserver = WebServer(strategy=strategy,
                                   processLibrary=FakedProcessLibrary,
                                   osLibrary=osLibrary)
        self.webserver.start()
        self.webserver.stop()
        assert self.webserver.process.poll() is None

    def test_isServerRunning(self, strategy=DjangoStrategy, osLibrary=FakedOSLibrary(os.name)):
        self.webserver = WebServer(strategy=strategy,
                                   processLibrary=FakedProcessLibrary,
                                   osLibrary=osLibrary)
        assert self.webserver.is_running() is False


class TestGunicornAppServer(TestDjangoWebServer):
    def test_startGunicornServer(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startServer(strategy=strategy, osLibrary=osLibrary)

    def test_startAndStopServer(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startAndStopServer(strategy=strategy, osLibrary=osLibrary)

    def test_isServerRunning(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_isServerRunning(strategy=strategy, osLibrary=osLibrary)


class TestGunicornNginxWebServer(TestGunicornAppServer):
    def test_startGnicornNginxServer(self, strategy=GunicornNginxStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startServer(strategy=strategy, osLibrary=osLibrary)

    def test_startAndStopServer(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startAndStopServer(strategy=strategy, osLibrary=osLibrary)

    def test_isServerRunning(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_isServerRunning(strategy=strategy, osLibrary=osLibrary)

    def test_configureServer(self):
        ports = {'nginx_port': 8091, 'gunicorn_port': 8092}
        FakedOSLibrary.name = 'posix'
        self.webserver = WebServer(strategy=GunicornNginxStrategy,
                                   processLibrary=FakedProcessLibrary,
                                   osLibrary=FakedOSLibrary,
                                   ports=ports)
        assert self.webserver.strategy.create_nginx_config(ports=ports, curled_ip_address="localhost") == """server{
    listen 8091;
    server_name BookStore;

    location /static/ {
        alias /var/www/static/;
    }
    location /static/imgs/ {
        alias /var/www/static/imgs/;
    }

    location / {
        proxy_pass http://localhost:8092;
    }
}
"""

    def test_curlIPAddress(self):
        ports = {'nginxPort': 8091, 'gunicornPort': 8092}
        FakedOSLibrary.name = 'posix'
        self.webserver = WebServer(strategy=GunicornNginxStrategy,
                                   processLibrary=FakedProcessLibrary,
                                   osLibrary=FakedOSLibrary,
                                   ports=ports)
        assert self.webserver.ip_address == "localhost"

    def test_store_cached_public_ip(self):
        ports = {'nginxPort': 8091, 'gunicornPort': 8092}
        FakedOSLibrary.name = 'posix'
        self.webserver = WebServer(strategy=GunicornNginxStrategy,
                                   processLibrary=FakedProcessLibrary,
                                   osLibrary=FakedOSLibrary,
                                   ports=ports)
        old_ip_file = self.webserver.temp_ip_address_file
        self.webserver2 = WebServer(strategy=GunicornNginxStrategy,
                                    processLibrary=FakedProcessLibrary,
                                    osLibrary=FakedOSLibrary,
                                    ports=ports)
        
        current_ip_file = self.webserver2.temp_ip_address_file
        assert current_ip_file == old_ip_file
