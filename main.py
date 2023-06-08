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
             Book('To Kill a Mockingbird', 'Harper Lee', '1960'),
             Book('The Lord of the Rings', 'J.R.R. Tolkien', '1954'),
             Book('The Great Gatsby', 'F. Scott Fitzgerald', '1925'),
             Book('Price and Prejudice', 'Jane Austen', '1813'),
             Book('Oedipus Rex (The Theban Plays, #1)', 'Sophocles', '1956'),
             Book('Moby-Dick', 'Herman Melville', '1851'),
             Book('The Adventures of Tom Sawyer', 'Mark Twain', '1876'),
             Book('The Canterbury Tales', 'Geoffrey Chaucer', '1392'),
             Book('Frankenstein: The 1818 Text', 'Mary Wollstonecraft Shelley', '1818')]
    defaultPort = 8091
    catalog = InMemoryCatalog()
    catalog.add(books)
    service = HTTPSocketService(catalog)
    server = SimpleSocketServer(service=service, port=defaultPort)
    server.start()
    lastCount = 0
    while server.getConnections() <= 20:
        if lastCount != server.getConnections():
            print("Connections: " + str(server.getConnections()))
            print("Body: " + str(server.service.lastResponse))
            lastCount += 1
    server.stop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sendRestFromClientHandleRestWithServer('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
