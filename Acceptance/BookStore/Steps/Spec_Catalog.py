from behave import given, when, then
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

def booksEqual(book, otherBook):
    return book == otherBook


def convertTableToArray(context):
    books = []
    for book in context.table:
        books.append({'Title': book[0], 'Author': book[1], 'Release year': book[2]})
    return books
