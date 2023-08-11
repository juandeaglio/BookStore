# This is a python webserver that serves a list of books to a web browser client.
import os
import subprocess

from Source.Book import Book
from Source.Catalog.InMemoryCatalog import InMemoryCatalog
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlInMemoryBooks import SqlInMemoryBooks
from Source.Server.Services.HTTPSocketService import HTTPSocketService
from Source.Server.SimpleSocketServer import SimpleSocketServer
from Source.WebServer import WebServer


def sendRestFromClientHandleRestWithServer(name):
    books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
             Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
             Book('To Kill a Mockingbird', 'Harper Lee', '1960'),
             Book('The Lord of the Rings', 'J.R.R. Tolkien', '1954'),
             Book('The Great Gatsby', 'F. Scott Fitzgerald', '1925'),
             Book('Pride and Prejudice', 'Jane Austen', '1813'),
             Book('Oedipus Rex', 'Sophocles', '1956'),
             Book('Moby-Dick', 'Herman Melville', '1851'),
             Book('The Adventures of Tom Sawyer', 'Mark Twain', '1876'),
             Book('The Canterbury Tales', 'Geoffrey Chaucer', '1392'),
             Book('Frankenstein: The 1818 Text', 'Mary Wollstonecraft Shelley', '1818')]
    SqlInMemoryBooks().clearCatalog()
    catalog = PersistentCatalog()
    catalog.add(books)
    booksArr = []
    with open("books/books.txt") as books:
        i = 0
        for line in books:
            line = line.strip()
            if i % 4 == 0:
                title = line
            elif i % 4 == 2:
                author = line
            elif i % 4 == 3:
                releaseYear = line
            i += 1
            if i % 4 == 0:
                booksArr.append(Book(title, author, releaseYear))

    web_server = WebServer()
    web_server.start()
    while True:
        continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sendRestFromClientHandleRestWithServer('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
