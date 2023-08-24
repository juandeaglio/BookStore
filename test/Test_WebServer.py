import os
import unittest
from Source.WebServer import WebServer
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy
from Source.WebServerStrategy.GunicornNginxStrategy import GunicornNginxStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy


class FakedOSLibrary:
    def __init__(self, name):
        self.name = name


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
            stdout=bytes("Works", encoding='utf-8')

        return ProcResults()

    def call(self):
        pass

    def Popen(self, args=None):
        if args is None:
            args = []

        return FakeProcess()


class TestDjangoWebServer(unittest.TestCase):
    def test_startDjangoServer(self, strategy=DjangoStrategy, osLibrary=FakedOSLibrary(os.name)):
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
        super().test_startDjangoServer(strategy, osLibrary)

    def test_startAndStopServer(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startAndStopServer(strategy, osLibrary)

    def test_isServerRunning(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_isServerRunning(strategy, osLibrary)


class TestGunicornNginxWebServer(TestGunicornAppServer):
    def test_startDjangoServer(self, strategy=GunicornNginxStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startDjangoServer(strategy, osLibrary)

    def test_startAndStopServer(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_startAndStopServer(strategy, osLibrary)

    def test_isServerRunning(self, strategy=GunicornStrategy, osLibrary=FakedOSLibrary(name='posix')):
        super().test_isServerRunning(strategy, osLibrary)
