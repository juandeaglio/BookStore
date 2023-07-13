import time

from behave import given, when, then
from Acceptance.BookStore.Steps.ContextTable import convertTableToArray
from Acceptance.BookStore.Steps.HTTPContent import convertContentToArray
from Source.Book import Book
from Acceptance.MockWebPage.TestRestClient import TestRestClient
from Source.Catalog.InMemoryCatalog import InMemoryCatalog


def arraysOfBooksAreTheSame(books, booksInCatalog):
    for book, otherBook in zip(books, booksInCatalog):
        if book != otherBook:
            print("1: " + book.title + " " + book.author + " " + book.releaseYear)
            print("2: " + otherBook.title + " " + otherBook.author + " " + otherBook.releaseYear)
            return False
    return True


@given('A catalog')
def defineCatalog(context):
    context.booksFromContext = convertTableToArray(context)
    context.catalog.add(context.booksFromContext)




@when('A user views the catalog')
def viewCatalog(context):
    response = TestRestClient.createClientThatGetsCatalogAsJson()
    context.jsonCatalog = response


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    fakeCatalog = InMemoryCatalog()
    fakeCatalog.add(books)
    books = fakeCatalog.getAllBooksJson()
    jsonBooks = context.jsonCatalog
    assert jsonBooks == books


# TODO re-do below tests to mimic above one.
@given('An empty catalog')
def defineCatalog(context):
    context.catalog.add([])


@when('The admin adds a book to the catalog')
def addBook(context):
    book = Book(title="Some Harry Potter Book, I think.", author="Just Kidding Rowling", releaseYear="1998")
    context.catalog.add([book])


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    response = TestRestClient.createClientThatGetsCatalog()
    context.booksInCatalog = convertContentToArray(response)

    assert 1 == len(context.booksInCatalog)


@when('The admin add a duplicate book to the catalog')
def addBook(context):
    alreadyAddedBook = context.booksFromContext[0]
    context.catalog.add([alreadyAddedBook])


@then('There will be no changes to the catalog')
def checkForExtraBook(context):
    response = TestRestClient.createClientThatGetsCatalogAsJson()
    context.booksInCatalog = response
    books = convertTableToArray(context)
    fakeCatalog = InMemoryCatalog()
    fakeCatalog.add(books)
    books = fakeCatalog.getAllBooksJson()

    assert len(books) == len(context.booksInCatalog)


