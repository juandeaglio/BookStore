from behave import given, when, then
from Source.BookStore import BookStore


@given('A catalog')
def step_given_storage_gateway_instance(context):
    # Create a basic catalog
    context.bookStore = BookStore()
