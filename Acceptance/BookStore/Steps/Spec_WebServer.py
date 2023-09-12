import os
import time

import requests.exceptions
import urllib3.exceptions
from behave import given, when, then

import BookStoreServer.settings
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
                or not isinstance(response1, requests.exceptions.ConnectionError) and response1.status_code == 200 \
                or not isinstance(response1, urllib3.exceptions.NewConnectionError):
            time.sleep(0.5)
            response2 = TestRestClient().createClientForAboutPage(port=context.port)

            assert isinstance(response2, requests.exceptions.ConnectTimeout) \
                   or not isinstance(response2, requests.exceptions.ConnectionError) \
                   or not isinstance(response2, urllib3.exceptions.NewConnectionError), \
                "Expected TimeoutError but got " + str(response2)

        else:
            assert isinstance(response1, requests.exceptions.ConnectTimeout) \
                   or not isinstance(response1, requests.exceptions.ConnectionError) \
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
        context.web_server.stop()
        assert context.response.status_code == 200, "Expected 200 OK but got " + str(context.response.status_code)
        assert context.response.headers['Content-Type'] == 'image/jpeg', "Expected image/png but got " + \
                                                                         str(context.response.headers['Content-Type'])


@given('The user hosts the web server on the public web')
def start_public_web_server(context):
    context.port = context.ports['nginxPort']
    GunicornNginxStrategy.port = context.port
    context.web_server = WebServer(strategy=GunicornNginxStrategy, ports=context.ports)
    context.public_ip_address = context.web_server.ip_address
    print("ip address is: " + context.public_ip_address)
    print("Config is: " + context.web_server.strategy.createNginxConfig(context.ports,
                                                                        curledIPAddress=context.public_ip_address))
    context.web_server.start()
    time.sleep(2)

    assert len(BookStoreServer.settings.ALLOWED_HOSTS) == \
           len(['.localhost', '127.0.0.1', '[::1]', 'localhost']) + 1
    assert len(BookStoreServer.settings.CORS_ORIGIN_WHITELIST) == \
           len(['http://localhost:3000', 'http://localhost:8091',
                'http://[::1]:3000']) + 1, "Expected 4 CORS but got " + \
                                           str(BookStoreServer.settings.ALLOWED_HOSTS)

    if (isinstance(context.web_server.strategy, GunicornNginxStrategy)) and os.name == 'nt':
        assert os.name == 'nt'
    else:
        assert context.web_server.isRunning() is True, "Expected web server to be up but it is down"


@then('The user can access the web page over the internet')
def access_public_web_server(context):
    if os.name == 'nt':
        assert os.name == 'nt'
    elif os.name == 'posix' and os.popen('whoami').read().strip() == 'runner':
        pass
    else:
        print("about to connect to: " + context.public_ip_address)
        response = TestRestClient().searchForBook("The Hobbit", port=context.port, host=context.public_ip_address)
        assert response.status_code == 200, "Expected 200 OK but got " + str(response.status_code)
        assert response.json() == [], "Expected empty json but got " + str(response.json)
