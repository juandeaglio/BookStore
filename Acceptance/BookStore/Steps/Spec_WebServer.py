import os
import time

import requests.exceptions
import urllib3.exceptions
from behave import given, when, then
from Acceptance.TestRestClient import TestRestClient
from Source.WebServer import WebServer
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy
from Source.WebServerStrategy.GunicornNginxStrategy import GunicornNginxStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy


strategies = {
    "Django": DjangoStrategy,
    "Gunicorn": GunicornStrategy,
    "GunicornNginx": GunicornNginxStrategy
}


@given('"{web_server_type}" web server is started')
def start_web_server(context, web_server_type):
    context.port = context.ports['nginxPort']
    GunicornNginxStrategy.port = context.port
    context.web_server = WebServer(strategy=strategies[web_server_type], ports=context.ports)
    context.web_server.start()
    context.web_server_type = web_server_type
    time.sleep(2)
    if context.web_server_type == "Gunicorn":
        context.port = context.ports['gunicornPort']
    else:
        context.port = context.ports['nginxPort']

    if (context.web_server_type == "Gunicorn" or context.web_server_type == "GunicornNginx") and os.name == 'nt':
        assert os.name == 'nt'
    else:
        assert context.web_server.isRunning() is True, "Expected web server to be up but it is down"


@then('The user can access the web page')
def accessWebPage(context):
    if os.name == 'nt' and (context.web_server_type == "Gunicorn" or context.web_server_type == "GunicornNginx"):
        assert os.name == 'nt'
    else:
        response = TestRestClient().searchForBook("The Hobbit", port=context.port)
        assert response.status_code == 200, "Expected 200 OK but got " + str(response.status_code)
        assert response.json() == [], "Expected empty json but got " + str(response.json)


@when('The user shuts down the web server')
def stopWebServer(context):
    if os.name == 'nt' and (context.web_server_type == "Gunicorn" or context.web_server_type == "GunicornNginx"):
        assert os.name == 'nt'
    else:
        context.web_server.stop()
        time.sleep(2)
        assert context.web_server.isRunning() is False, "Expected web server to be down but it is still running."


@then('The user can no longer access the web page')
def accessWebPage(context):
    if os.name == 'nt' and (context.web_server_type == "Gunicorn" or context.web_server_type == "GunicornNginx"):
        assert os.name == 'nt'
    else:
        response1 = TestRestClient().createClientForAboutPage(port=context.port)

        # if response 1 is not an exception and the status code is 200, then wait 0.5 seconds and try again
        print(response1)
        print(type(response1))
        if not isinstance(response1, requests.exceptions.ConnectTimeout) \
                or not isinstance(response1, requests.exceptions.ConnectionError) and response1.status_code == 200\
                or not isinstance(response1, urllib3.exceptions.NewConnectionError):
            time.sleep(0.5)
            response2 = TestRestClient().createClientForAboutPage(port=context.port)

            assert isinstance(response2, requests.exceptions.ConnectTimeout) \
                or not isinstance(response2, requests.exceptions.ConnectionError)\
                or not isinstance(response2, urllib3.exceptions.NewConnectionError), \
                "Expected TimeoutError but got " + str(response2)

        else:
            assert isinstance(response1, requests.exceptions.ConnectTimeout) \
                or not isinstance(response1, requests.exceptions.ConnectionError)\
                or not isinstance(response1, urllib3.exceptions.NewConnectionError), \
                "Expected TimeoutError but got " + str(response1)


@when('The user fetches a static image')
def fetchStaticImage(context):
    if os.name == 'nt' and (context.web_server_type == "Gunicorn" or context.web_server_type == "GunicornNginx"):
        assert os.name == 'nt'
    else:
        context.response = TestRestClient().fetchStaticImage(port=context.port)


@then('The user can see the static image')
def seeStaticImage(context):
    if os.name == 'nt' and (context.web_server_type == "GunicornNginx"):
        assert os.name == 'nt'
    else:
        print(context.web_server.inspectedConfigFile)
        assert context.response.status_code == 200, "Expected 200 OK but got " + str(context.response.status_code)
        assert context.response.headers['Content-Type'] == 'image/jpeg', "Expected image/png but got " + \
                                                                        str(context.response.headers['Content-Type'])