from behave import given, when, then

from Source.Book import Book
from Source.PersistentCatalog import PersistentCatalog
from Source.BookStore import BookStore


@given('A catalog')
def defineCatalog(context):
    context.catalog = PersistentCatalog()
    books = convertTableToArray(context)
    context.catalog.add(books)


@when('I view the catalog')
def viewCatalog(context):
    context.booksInCatalog = context.catalog.getAllBooks()


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    assert books == context.booksInCatalog


@given('An empty catalog')
def defineCatalog(context):
    context.catalog = PersistentCatalog()


@when('I add a book to the catalog')
def addBook(context):
    book = Book(title="Harry Potter 1", author="J.K. Rowling", releaseYear="1991")
    context.catalog.add([book])


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    assert len(context.catalog.getAllBooks()) == 1


@when('I add a duplicate book to the catalog')
def addBook(context):
    book = Book(title="The Hunger Games", author="Suzanne Collins", releaseYear="2008")
    context.catalog.add([book])


@then('There will be no changes to the catalog')
def checkForExtraBook(context):
    assert len(context.catalog.getAllBooks()) == 3


def convertTableToArray(context):
    books = []
    for book in context.table:
        books.append(Book(title=book[0], author=book[1], releaseYear=book[2]))

    return books
