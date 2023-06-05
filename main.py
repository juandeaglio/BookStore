# This is a sample Python script.
from Acceptance.MockWebPage.TestRestClient import TestRestClient
from Source.Book import Book
from Source.Catalog.InMemoryCatalog import InMemoryCatalog
from Source.SocketServer.Services.HTTPSocketService import HTTPSocketService
from Source.SocketServer.SimpleSocketServer import SimpleSocketServer


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def sendRestFromClientHandleRestWithServer(name):
    books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
             Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
             Book('To Kill a Mockingbird', 'Harper Lee', '1960')]
    defaultPort = 8091
    catalog = InMemoryCatalog()
    catalog.add(books)
    service = HTTPSocketService(catalog)
    server = SimpleSocketServer(service=service, port=defaultPort)
    server.start()
    response = TestRestClient.createClientThatGetsCatalog()
    print(str(response))
    server.stop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sendRestFromClientHandleRestWithServer('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
