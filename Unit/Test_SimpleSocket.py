import socket
import threading
import time
import unittest

from Source.SimpleSocketServer import SimpleSocketServer
from Source.FakeSocketService import FakeSocketService


class SimpleSocketTest(unittest.TestCase):
    def setUp(self):
        self.port = 8091
        self.service = FakeSocketService()
        self.server = SimpleSocketServer(service=self.service, port=self.port)

    def tearDown(self):
        self.server.stop()

    def test_canStartAndStopServer(self):
        self.server.start()
        assert self.server.isRunning()
        self.server.stop()
        assert not self.server.isRunning()

    def test_canAcceptIncomingConnection(self):
        self.server.start()
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(("localhost", self.port))
        assert self.server.getConnections() == 1
        self.server.stop()


if __name__ == '__main__':
    unittest.main()
