from behave import given, when, then, step
from Source.Book import Book
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.StorageGateway import StorageGateway
from test.BooksForTest import booksForTest


@given('A user added books to the catalog')
def add_books_to_catalog(context):
    context.books = booksForTest
    context.type = SqlBookDatabase
    SqlBookDatabase().clearCatalog()
    context.storageGateway = StorageGateway(context.type())
    context.storageGateway.add(context.books)


@when('The catalog is accessed')
def persistence_with_synchronize(context):
    newStorageGateway = StorageGateway(context.type())
    newStorageGateway.add(Book(title="Test", author="Test", releaseYear="2000",
                               price="0", imagePath="", description=""))
    context.retVals = newStorageGateway.fetchBooksFromDatabase()


@then('The user can see the books in the catalog')
def compare_books(context):
    assert len(context.retVals) == len(context.storageGateway.fetchBooksFromDatabase())

