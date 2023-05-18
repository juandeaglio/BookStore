from behave import given, when, then
from Source.BookStore import BookStore
import pytest

from Source.Catalog import Catalog
from Source.InMemoryDatabase import InMemoryDatabase


@given('A catalog')
def defineCatalog(context):
    context.bookStore = BookStore(Catalog(InMemoryDatabase()))
    books = convertTableToArray(context)
    context.bookStore.addToCatalog(books)


@when('I view the catalog')
def viewCatalog(context):
    context.booksInCatalog = context.bookStore.getCatalog()


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    for element, otherElement in zip(books, context.bookStore.getCatalog()):
        print(str(element) + '\t' + str(otherElement))
        assert theSame(element, otherElement)


def theSame(book, otherBook):
    return book == otherBook


def convertTableToArray(context):
    books = []
    for book in context.table:
        books.append({'Title': book[0], 'Author': book[1], 'Year': book[2]})
    return books
