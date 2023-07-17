import time

from behave import given, when, then
from Acceptance.BookStore.Steps.ContextTable import convertTableToArray
from Acceptance.BookStore.Steps.HTTPContent import convertContentToArray
from Source.Book import Book
from Acceptance.MockWebPage.TestRestClient import TestRestClient
from Source.Catalog.InMemoryCatalog import InMemoryCatalog


@given('An empty catalog')
def defineCatalog(context):
    context.catalog.add([])


@when('The admin adds a book to the catalog')
def addBook(context):
    assert TestRestClient.asAdminAddBook() == 200


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    response = TestRestClient.createClientThatGetsCatalogAsJson()
    context.booksInCatalog = response

    assert 1 == len(context.booksInCatalog)