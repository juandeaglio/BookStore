import time
from operator import eq

from behave import given, when, then
from Acceptance.TestRestClient import TestRestClient
from Source.Catalog.InMemoryCatalog import InMemoryCatalog

from Source.Book import Book


class WebServer:
    def __init__(self, strategy):
        self.strategy = strategy
        self.process = None

    def start(self):
        pass

    def stop(self):
        pass

    def isRunning(self):
        pass


@given('A user starts the "{web_server_type}" web server')
def start_web_server(context, web_server_type):
    context.web_server = WebServer(strategy=web_server_type)
    context.web_server.start()


@then('The user can access the web page')
def accessWebPage(context):
    time.sleep(2)
    response = TestRestClient().createClientForAboutPage(timeout=2)
    assert "about" in response.text.lower()
    assert response.status_code == 200, "Expected 200 OK but got " + str(response.status_code)


@when('The user shuts down the web server')
def stopWebServer(context):
    context.web_server.stop()
    assert context.web_server.isRunning() is False, "Expected web server to be down but it is still running."


@then('The user can no longer access the web page')
def accessWebPage(context):
    try:
        response1 = TestRestClient().createClientForAboutPage()

        # server still shutting down
        if response1.status_code == 200:
            time.sleep(0.5)
            response2 = TestRestClient().createClientForAboutPage()

            assert response2.status_code != 200, "Server still returning 200 OK after multiple checks."

    except (ConnectionError, TimeoutError):
        return  # Server seems down. Test passed.
