import time
from operator import eq

from behave import given, when, then
from Acceptance.TestRestClient import TestRestClient
from Source.Catalog.InMemoryCatalog import InMemoryCatalog

from Source.Book import Book


@given('A user starts the "{web_server_type}" web server')
def start_web_server(context, web_server_type):
    context.web_server = WebServer(strategy=web_server_type)
    context.web_server.start()


@then('The user can access the web page')
def accessWebPage(context):
    response = TestRestClient().getWebPage()
    assert response.status_code == 200, "Expected 200 OK but got " + str(response.status_code)


@when('The user shuts down the web server')
def stopWebServer(context):
    context.web_server.stop()


@then('The user can no longer access the web page')
def accessWebPage(context):
    try:
        response1 = TestRestClient().getWebPage()

        # server still shutting down
        if response1.status_code == 200:
            time.sleep(0.5)
            response2 = TestRestClient().getWebPage()

            assert response2.status_code != 200, "Server still returning 200 OK after multiple checks."

    except (ConnectionError, TimeoutError):
        return  # Server seems down. Test passed.
