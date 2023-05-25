import random
import socket
import string
import threading
import unittest
import concurrent.futures
from Source.SimpleSocketServer import SimpleSocketServer
from Source.FakeSocketService import FakeSocketService


def aggregateServerResponsesToArray(futures):
    responses = []
    for i in range(0,len(futures)):
        responses.append(("client"+str(i), futures[i].result().recv(1024).decode("UTF-8")))

    return responses


def generateRandomStrings():
    strings = []
    for i in range(0, 10):
        strings.append(("client"+str(i), ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))))

    return strings

class SimpleSocketTest(unittest.TestCase):
    def setUp(self):
        self.port = 8091
        self.service = FakeSocketService()
        self.server = SimpleSocketServer(service=self.service, port=self.port)
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_startAndStopServer(self):
        assert self.server.isRunning()
        self.server.stop()
        assert not self.server.isRunning()

    def test_acceptIncomingConnection(self):
        createClient(self.port)
        self.server.stop()
        assert self.server.getConnections() == 1

    def test_acceptMultipleIncomingConnection(self):
        expectedConnections = 100
        for i in range(0, expectedConnections):
            createClient(self.port)
        self.server.stop()
        assert self.server.getConnections() == expectedConnections

    def test_sendAndReceiveData(self):
        client = createClientWithMessage("hello", self.port)
        assert client.recv(1024).decode("UTF-8") == "hello"

    def test_sendAndReceiveDataMultipleConnections(self):
        expectedMsgs = generateRandomStrings()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(createClientWithMessage, param[1]) for param in expectedMsgs]

            msgs = aggregateServerResponsesToArray(futures)
            assert expectedMsgs == msgs


def createClientWithMessage(expectedMessage3="", port=8091):
    client3 = createClient(port)
    client3.send(expectedMessage3.encode("UTF-8"))
    return client3


def createClient(port):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("localhost", port))
    return clientSocket


if __name__ == '__main__':
    unittest.main()
