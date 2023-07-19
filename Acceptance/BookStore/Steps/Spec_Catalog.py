from operator import eq

from behave import given, when, then
from Acceptance.BookStore.Steps.ContextTable import convertTableToArray
from Acceptance.TestRestClient import TestRestClient
from Source.Catalog.InMemoryCatalog import InMemoryCatalog


def createExpectedJson(books):
    fakeCatalog = InMemoryCatalog()
    fakeCatalog.add(books)
    books = fakeCatalog.getAllBooksJson()
    return books


@given('A catalog')
def defineCatalog(context):
    context.booksFromContext = convertTableToArray(context)
    context.catalog.add(context.booksFromContext)


@when('A user views the catalog')
def viewCatalog(context):
    response = TestRestClient().createClientThatGetsCatalogAsJson()
    context.jsonCatalog = response


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    books = createExpectedJson(books)
    jsonBooks = context.jsonCatalog
    assert jsonBooks == books


@given('A user has admin permissions')
def createAdminUser(context):
    #add user as admin
    pass

@when('A user logs in as an admin')
def loginAsAdmin(context):
    context.statusCode = TestRestClient().createClientAsAdmin()


@then('The user can access admin pages')
def loggedInAsAdmin(context):
    assert 200 == context.statusCode


@when('The admin add a duplicate book to the catalog')
def addBook(context):
    alreadyAddedBook = context.booksFromContext[0]
    assert TestRestClient().createClientAsAdminAddBook(book=alreadyAddedBook) == 200


@then('There will be no changes to the catalog')
def checkForExtraBook(context):
    response = TestRestClient().createClientThatGetsCatalogAsJson()
    books = convertTableToArray(context)
    books = createExpectedJson(books)
    assert len(books) == len(response)


@when('A user searches for Harry Potter')
def addBook(context):
    response = TestRestClient().searchForBook(title="Harry Potter")
    assert response.status_code == 200
    context.jsonBooks = response.json()

@then('Relevant results are displayed')
def checkForExtraBook(context):
    books = convertTableToArray(context)
    books = createExpectedJson(books)
    print("books:\n" + str(books))
    print("jsonBooks:\n" + str(context.jsonBooks))
    assert eq(context.jsonBooks, books)
