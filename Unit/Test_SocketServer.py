import random
import string
import unittest
import concurrent.futures

import requests

from Source.Book import Book
from Source.Catalog.InMemoryCatalog import InMemoryCatalog
from Source.BookStore import BookStore
from Source.SocketServer.ClosingSocketService import ClosingSocketService
from Source.SocketServer.HTTPSocketService import HTTPSocketService
from Source.SocketServer.SimpleSocketServer import SimpleSocketServer
from Source.SocketServer.EchoSocketService import EchoSocketService
from Unit.Client import Client


def aggregateServerResponsesToArray(futures):
    responses = []
    for i in range(0, len(futures)):
        responses.append(("client" + str(i), futures[i].result().recv(1024).decode("UTF-8")))

    return responses


def generateRandomStrings():
    strings = []
    for i in range(0, 10):
        strings.append(("client" + str(i), ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))))

    return strings


class StoppingSocketTest(unittest.TestCase):
    def setUp(self):
        self.port = 8091
        self.service = ClosingSocketService()
        self.server = SimpleSocketServer(service=self.service, port=self.port)

    def test_startAndStopServer(self):
        self.server.start()
        assert self.server.isRunning()
        self.server.stop()
        assert not self.server.isRunning()


class SimpleSocketTest(unittest.TestCase):
    def setUp(self):
        self.port = 8091
        self.service = ClosingSocketService()
        self.server = SimpleSocketServer(service=self.service, port=self.port)
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_acceptIncomingConnection(self):
        Client.createClient(self.port).recv(1)
        assert self.server.getConnections() == 1

    def test_acceptMultipleIncomingConnection(self):
        expectedConnections = 100
        for i in range(0, expectedConnections):
            Client.createClient(self.port).recv(1)
        assert self.server.getConnections() == expectedConnections


class EchoSocketTest(unittest.TestCase):
    def setUp(self):
        self.port = 8091
        self.service = EchoSocketService()
        self.server = SimpleSocketServer(service=self.service, port=self.port)
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_sendAndReceiveData(self):
        client = Client.createClientWithMessage("hello", self.port)
        assert client.recv(1024).decode("UTF-8") == "hello"

    def test_sendAndReceiveDataMultipleConnections(self):
        expectedMsgs = generateRandomStrings()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(Client.createClientWithMessage, param[1]) for param in expectedMsgs]

            msgs = aggregateServerResponsesToArray(futures)
            assert expectedMsgs == msgs


def parse(responseData):
    string = ''
    for line in responseData:
        string+=line +'\n'

    return string


# TODO not a small enough test
class RestSocketTest(unittest.TestCase):
    def setUp(self) -> None:
        self.books = [Book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "1999"),
                      Book("Harry Potter Prisoner of Azkaban", "J.K. Rowling", "2001"),
                      Book("Harry Potter Chamber of Secrets", "J.K. Rowling", "2002")]
        self.bookStore = BookStore(InMemoryCatalog())
        self.bookStore.addToCatalog(self.books)
        self.service = HTTPSocketService(self.bookStore)
        self.server = SimpleSocketServer(service=self.service, port=8091)
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_sendAndReceiveData(self):
        expectedResponse = self.bookStore.getCatalogToString()
        responseData = requests.get("http://127.0.0.1:8091/getCatalog").text.splitlines()
        parsedData = parse(responseData)
        assert expectedResponse == parsedData


if __name__ == '__main__':
    unittest.main()
