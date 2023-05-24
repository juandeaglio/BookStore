from behave import given, when, then

from Source.RestGateway import RestGateway
from Source.Book import Book
from Source.Catalog.PersistentCatalog import PersistentCatalog


@given('A catalog')
def defineCatalog(context):
    context.restGateway = RestGateway()
    context.restGateway.listens()
    context.simpleSocketService = SimpleSocketService("127.0.0.1", 9191)

    context.catalog = PersistentCatalog()
    books = convertTableToArray(context)
    context.catalog.add(books)


@when('A user views the catalog')
def viewCatalog(context):
    while not context.restGateway.listening:
        if isinstance(context.restGateway.requestType, GetCatalog()):
            context.booksInCatalog = context.catalog.getAllBooks()


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    assert books == context.booksInCatalog


@given('An empty catalog')
def defineCatalog(context):
    context.restGateway = RestGateway()
    context.restGateway.listens()
    context.simpleSocketService = SimpleSocketService("127.0.0.1", 9191)

    context.catalog = PersistentCatalog()


@when('The admin adds a book to the catalog')
def addBook(context):
    while not context.restGateway.listening:
        if isinstance(context.restGateway.requestType, AddToCatalog("Harry Potter 1", "J.K. Rowling", "1991")):
            book = Book(context.restGateway.requestBody)
            context.catalog.add([book])


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    assert len(context.catalog.getAllBooks()) == 1


@when('The admin add a duplicate book to the catalog')
def addBook(context):
    while not context.restGateway.listening:
        if isinstance(context.restGateway.requestType, AddToCatalog("The Hunger Games", "Suzanne Collins", "2008")):
            book = Book(context.restGateway.requestBody)
            context.catalog.add([book])


@then('There will be no changes to the catalog')
def checkForExtraBook(context):
    assert len(context.catalog.getAllBooks()) == 3


def convertTableToArray(context):
    books = []
    for book in context.table:
        books.append(Book(title=book[0], author=book[1], releaseYear=book[2]))

    return books
