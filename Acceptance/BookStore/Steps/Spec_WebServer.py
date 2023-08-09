import time

import requests.exceptions
import urllib3.exceptions
from behave import given, when, then
from Acceptance.TestRestClient import TestRestClient
from Source.WebServer import WebServer


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
    response1 = TestRestClient().createClientForAboutPage()

    # if response 1 is not an exception and the status code is 200, then wait 0.5 seconds and try again
    print(response1)
    print(type(response1))
    if not isinstance(response1, requests.exceptions.ConnectTimeout) \
            or not isinstance(response1, requests.exceptions.ConnectionError) and response1.status_code == 200\
            or not isinstance(response1, urllib3.exceptions.NewConnectionError):
        time.sleep(0.5)
        response2 = TestRestClient().createClientForAboutPage()

        assert isinstance(response2, requests.exceptions.ConnectTimeout) \
            or not isinstance(response2, requests.exceptions.ConnectionError)\
            or not isinstance(response2, urllib3.exceptions.NewConnectionError), \
            "Expected TimeoutError but got " + str(response2)

    else:
        assert isinstance(response1, requests.exceptions.ConnectTimeout) \
            or not isinstance(response1, requests.exceptions.ConnectionError)\
            or not isinstance(response1, urllib3.exceptions.NewConnectionError), \
            "Expected TimeoutError but got " + str(response1)
