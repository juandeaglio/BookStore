from behave import given, when, then

from Source.RestMessage import RestMessage
from Source.Book import Book
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Acceptance.RestClient import RestClient


@given('A catalog')
def defineCatalog(context):
    books = convertTableToArray(context)
    context.bookStore.addToCatalog(books)


class GetCatalogRestMessage(RestMessage):
    def __init__(self):
        self.method = 'GET'
        self.body = None
        self.path = '/catalog'


@when('A user views the catalog')
def viewCatalog(context):
    context.client = RestClient.createClientThatGetsCatalog(context.defaultPort)
    context.client.send(GetCatalogRestMessage())
    context.booksInCatalog = convertJsonToArray(context.client.getResponse().body)


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    assert books == context.booksInCatalog
    context.server.stop()


#TODO re-do below tests to mimic above one.
@given('An empty catalog')
def defineCatalog(context):
    #context.simpleSocketService = SimpleSocketServer("127.0.0.1", 9191)
    context.catalog = PersistentCatalog()


@when('The admin adds a book to the catalog')
def addBook(context):
    assert 1==0 # not impelmented

@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    assert len(context.catalog.getAllBooks()) == 1


@when('The admin add a duplicate book to the catalog')
def addBook(context):
    assert 1 == 0  # not impelmented


@then('There will be no changes to the catalog')
def checkForExtraBook(context):
    assert len(context.catalog.getAllBooks()) == 3


def convertTableToArray(context):
    books = []
    for book in context.table:
        books.append(Book(title=book[0], author=book[1], releaseYear=book[2]))

    return books
