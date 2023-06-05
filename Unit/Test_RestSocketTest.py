import unittest

import requests

from Acceptance.MockWebPage.TestRestClient import TestRestClient
from Source.Book import Book
from Source.Catalog.InMemoryCatalog import InMemoryCatalog
from Source.SocketServer.Services.HTTPSocketService import HTTPSocketService
from Source.SocketServer.SimpleSocketServer import SimpleSocketServer
from Unit.TestClientSocket import TestClientSocket


class RestSocketTest(unittest.TestCase):
    def setUp(self) -> None:
        self.books = [Book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "1999"),
                      Book("Harry Potter Prisoner of Azkaban", "J.K. Rowling", "2001"),
                      Book("Harry Potter Chamber of Secrets", "J.K. Rowling", "2002")]
        self.catalog = InMemoryCatalog()
        self.catalog.add(self.books)
        self.service = HTTPSocketService(self.catalog)
        self.port = 8091
        self.server = SimpleSocketServer(service=self.service, port=self.port)
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_sendAndReceiveData(self):
        expectedHTTP = bytes("HTTP/1.1 200 OK\n" + "Content-Length: " + \
                             str(len(self.catalog.toString())) + "\n" + \
                             "\n" + self.catalog.toString(), "UTF-8")
        self.service.serve(TestClientSocket())
        responseData = self.service.lastResponse
        assert expectedHTTP == responseData

    def test_sendRequestWhileClosing(self):
        self.server.stop()
        try:
            TestRestClient.createClientThatGetsCatalog()
        except requests.exceptions.ConnectTimeout as e:
            print(str(e))
        self.assertRaises(requests.exceptions.ConnectTimeout, TestRestClient.createClientThatGetsCatalog)
