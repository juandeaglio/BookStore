import os
import unittest
from Source.WebServer import WebServer
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy
from Source.WebServerStrategy.GunicornNginxStrategy import GunicornNginxStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy


class FakedOSLibrary:
    def __init__(self, name=os.name):
        self.name = name

    @staticmethod
    def getcwd():
        return "D:/PyCharmProjs/BookStore"

    @staticmethod
    def popen(cmd):
        class Data:
            def read(self):
                return "localhost%20"

        return Data()

class FakeProcess:
    def terminate(self):
        pass

    def kill(self):
        pass

    def poll(self):
        return None


class FakedProcessLibrary:
    def run(self, args=None, capture_output=True, check=True):
        class ProcResults:
            returncode = 0
            stdout = bytes("localhost", encoding='utf-8')

        return ProcResults()

    def call(self):
        pass

    def Popen(self, args=None):
        if args is None:
            args = []

        return FakeProcess()


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
        assert self.webserver.isRunning() is False


class TestGunicornAppServer(TestDjangoWebServer):
    def test_startGunicornServer(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startServer(strategy, osLibrary)

    def test_startAndStopServer(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startAndStopServer(strategy, osLibrary)

    def test_isServerRunning(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_isServerRunning(strategy, osLibrary)


class TestGunicornNginxWebServer(TestGunicornAppServer):
    def test_startGnicornNginxServer(self, strategy=GunicornNginxStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startServer(strategy, osLibrary)

    def test_startAndStopServer(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startAndStopServer(strategy, osLibrary)

    def test_isServerRunning(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_isServerRunning(strategy, osLibrary)

    def test_configureServer(self):
        ports = {'nginxPort': 8091, 'gunicornPort': 8092}
        FakedOSLibrary.name = 'posix'
        self.webserver = WebServer(strategy=GunicornNginxStrategy,
                                   processLibrary=FakedProcessLibrary,
                                   osLibrary=FakedOSLibrary,
                                   ports=ports)
        assert self.webserver.strategy.createNginxConfig(ports, curledIPAddress="localhost") == """server{
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
        assert self.webserver.strategy.curlIPAddress() == "localhost"

