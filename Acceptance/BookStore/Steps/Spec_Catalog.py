from operator import eq

from behave import given, when, then, step
from Acceptance.TestRestClient import TestRestClient
from Source.Catalog.InMemoryCatalog import InMemoryCatalog

from Source.Book import Book


def convertTableToArray(context):
    books = []
    #reflect on the book object from context.table and compare all columns
    for book in context.table:
        new = Book()
        #use the index of the column to get the attribute name
        for index, attribute in enumerate(context.table.headings):
            setattr(new, new.attributes[index], book[index])

        books.append(new)

    return books


def createExpectedJson(books):
    fakeCatalog = InMemoryCatalog()
    fakeCatalog.add(books)
    books = fakeCatalog.booksToJson(fakeCatalog.getAllBooks())
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
    print("context.jsonCatalog" + str(context.jsonCatalog))
    print("books" + str(books))
    assert context.jsonCatalog == books


@given('A user has admin permissions')
def createAdminUser(context):
    # add user as admin
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
    print("actual response" + str(response))
    print("expected" + str(books))
    assert len(books) == len(response)


@when('A user searches for Harry Potter')
def searchForBookTitle(context):
    response = TestRestClient().searchForBook(title="Harry Potter", timeout=2)
    assert response.status_code == 200
    print("response" + str(response.json()))
    context.jsonBooks = response.json()


@then('Relevant results are displayed')
def bookFound(context):
    books = convertTableToArray(context)
    books = createExpectedJson(books)
    print("expected" + str(books))
    assert eq(context.jsonBooks, books)


@when('An authorized user deletes the first book in the catalog')
def searchForBookTitle(context):
    firstBook = context.booksFromContext[0]
    response = TestRestClient().deleteBook(firstBook)
    assert response == 200
    context.jsonBooks = TestRestClient().createClientThatGetsCatalogAsJson()
