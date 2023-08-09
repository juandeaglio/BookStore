import unittest
from Source.WebServer import WebServer


class FakedOSLibrary:
    def __init__(self):
        self.name = 'None'


class FakedProcessLibrary:
    def run(self):
        pass

    def call(self):
        pass

    def Popen(self, args=None):
        if args is None:
            args = []


class TestInMemoryStorageGateway(unittest.TestCase):
    def test_startAndStopServer(self):
        self.web_server = WebServer(strategy="Django", processLibrary=FakedProcessLibrary, osLibrary=FakedOSLibrary())
        self.web_server.start()
        assert self.web_server.isRunning() is True, "Expected web server to be running but it is not."
        self.web_server.stop()
        assert self.web_server.isRunning() is False, "Expected web server to be down but it is still running."
