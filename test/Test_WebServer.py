import unittest
from Source.WebServer import WebServer
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy


class FakedOSLibrary:
    def __init__(self):
        self.name = 'None'


class FakeProcess:
    def terminate(self):
        pass

    def kill(self):
        pass

    def poll(self):
        return None


class FakedProcessLibrary:
    def run(self, args=None, capture_output=True):
        class ProcResults:
            returncode = 0

        return ProcResults()

    def call(self):
        pass

    def Popen(self, args=None):
        if args is None:
            args = []

        return FakeProcess()


class TestWebServer(unittest.TestCase):
    def test_startDjangoServer(self):
        self.webserver = WebServer(strategy=DjangoStrategy,
                                   processLibrary=FakedProcessLibrary(),
                                   osLibrary=FakedOSLibrary())
        self.webserver.start()
        assert self.webserver.process is not None

    def test_startAndStopDjangoServer(self):
        self.webserver = WebServer(strategy=DjangoStrategy,
                                   processLibrary=FakedProcessLibrary(),
                                   osLibrary=FakedOSLibrary())
        self.webserver.start()
        self.webserver.stop()
        assert self.webserver.process.poll() is None

    def test_isServerRunning(self):
        self.webserver = WebServer(strategy=DjangoStrategy,
                                   processLibrary=FakedProcessLibrary(),
                                   osLibrary=FakedOSLibrary())
        assert self.webserver.isRunning() is False
