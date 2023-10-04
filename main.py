# This is a python webserver that serves a list of books to a web browser client.
from ExampleDescriptions import exampleDescriptions
from Source.Book import Book
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.WebServer import WebServer
from Source.WebServerStrategy.GunicornNginxStrategy import GunicornNginxStrategy


def sendRestFromClientHandleRestWithServer(name):
    catalog = PersistentCatalog()
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

        catalog.add(booksArr)
    except:
        pass
    ports = {'nginxPort': 8091, 'gunicornPort': 8092}
    web_server = WebServer(ports=ports, strategy=GunicornNginxStrategy)
    public_ip_address = web_server.ip_address
    web_server.strategy.create_nginx_config(ports=ports, curled_ip_address=public_ip_address)
    web_server.start()
    while True:
        continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sendRestFromClientHandleRestWithServer('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
