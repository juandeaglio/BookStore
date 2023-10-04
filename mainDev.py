# This is a python webserver that serves a list of books to a web browser client.

from Source.ExampleDescriptions import exampleDescriptions
from Source.Book import Book
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.WebServer import WebServer
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy


def sendRestFromClientHandleRestWithServer(name):
    books = [Book(title='The Hunger Games', author='Suzanne Collins', releaseYear='2008',
                  imagePath="static/imgs/The Hunger Games.jpg", description=exampleDescriptions[0], price="5.50"),
             Book(title='Harry Potter and the Sorcerer\'s Stone', author='J.K. Rowling', releaseYear='1998',
                  imagePath="static/imgs/Harry Potter and the Sorcerer's Stone.jpg", description=exampleDescriptions[1],
                  price="5.60"),
             Book(title='To Kill a Mockingbird', author='Harper Lee', releaseYear='1960',
                  imagePath="static/imgs/To Kill a Mockingbird.jpg", description=exampleDescriptions[2], price="5.70"),
             Book(title='The Lord of the Rings', author='J.R.R. Tolkien', releaseYear='1954',
                  imagePath="static/imgs/The Lord of the Rings.jpg", description=exampleDescriptions[3], price="5.80"),
             Book(title='The Great Gatsby', author='F. Scott Fitzgerald', releaseYear='1925',
                  imagePath="static/imgs/The Great Gatsby.jpg", description=exampleDescriptions[4], price="5.90"),
             Book(title='Pride and Prejudice', author='Jane Austen', releaseYear='1813',
                  imagePath="static/imgs/Pride and Prejudice.jpg", description=exampleDescriptions[5], price="6.00"),
             Book(title='Oedipus Rex', author='Sophocles', releaseYear='1956', imagePath="static/imgs/Oedipus Rex.jpg",
                  description=exampleDescriptions[6], price="6.10"),
             Book(title='Moby-Dick', author='Herman Melville', releaseYear='1851',
                  imagePath='static/imgs/Moby-Dick.jpg', description=exampleDescriptions[7], price="6.20"),
             Book(title='The Adventures of Tom Sawyer', author="Mark Twain", releaseYear="1876",
                  imagePath='static/imgs/The Adventures of Tom Sawyer.jpg', description=exampleDescriptions[8],
                  price="6.30"),
             Book(title='The Canterbury Tales', author='Geoffrey Chaucer', releaseYear='1392',
                  imagePath="static/imgs/The Canterbury Tales.jpg", description=exampleDescriptions[9], price='6.40'),
             Book(title='Frankenstein: The 1818 Text', author='Mary Wollstonecraft Shelley', releaseYear='1818',
                  imagePath="static/imgs/Frankenstein: The 1818 Text", description=exampleDescriptions[10],
                  price='6.50')
             ]
    SqlBookDatabase().clear_catalog()
    catalog = PersistentCatalog()
    catalog.add(books)
    booksArr = []
    try:
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
    except:
        pass
    ports = {'nginxPort': 8091, 'gunicornPort': 8092}
    web_server = WebServer(ports=ports, strategy=DjangoStrategy)
    public_ip_address = web_server.ip_address
    web_server.start()
    while True:
        continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sendRestFromClientHandleRestWithServer('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
