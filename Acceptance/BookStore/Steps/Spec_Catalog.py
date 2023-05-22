from behave import given, when, then

from Source.Book import Book
from Source.Catalog import Catalog
from Source.BookStore import BookStore


@given('A catalog')
def defineCatalog(context):
    context.bookStore = BookStore(Catalog())
    books = convertTableToArray(context)
    context.bookStore.addToCatalog(books)


@when('I view the catalog')
def viewCatalog(context):
    context.booksInCatalog = context.bookStore.getCatalog()


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    assert books == context.bookStore.getCatalog()


@given('An empty catalog')
def defineCatalog(context):
    context.bookStore = BookStore(Catalog())


@when('I add a book to the catalog')
def addBook(context):
    book = Book(title="Harry Potter 1", author="J.K. Rowling", releaseYear="1991")
    context.bookStore.addToCatalog([book])


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    assert len(context.bookStore.getCatalog()) == 1

def booksEqual(book, otherBook):
    return book == otherBook


def convertTableToArray(context):
    books = []
    for book in context.table:
        books.append(Book(title=book[0], author=book[1], releaseYear=book[2]))

    return books
