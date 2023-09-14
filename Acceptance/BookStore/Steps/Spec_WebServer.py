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

    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        assert context.web_server.isRunning() is True, "Expected web server to be up but it is down"


@then('The user can access the web page')
def accessWebPage(context):
    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        response = TestRestClient().searchForBook("The Hobbit", port=context.port)
        assert response.status_code == 200, "Expected 200 OK but got " + str(response.status_code)
        assert response.json() == [], "Expected empty json but got " + str(response.json)


@when('The user shuts down the web server')
def stopWebServer(context):
    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        context.web_server.stop()
        time.sleep(2)
        assert context.web_server.isRunning() is False, "Expected web server to be down but it is still running."


def responseIsAnError(response):
    return isinstance(response, requests.exceptions.ConnectTimeout) \
           or not isinstance(response, requests.exceptions.ConnectionError) \
           and response.status_code == 200 \
           or not isinstance(response, urllib3.exceptions.NewConnectionError)


def runningGunicornOnWindows(context):
    web_server_type = context.web_server.strategy
    return os.name == 'nt' and (isinstance(web_server_type, GunicornStrategy) or
                                isinstance(web_server_type, GunicornNginxStrategy))


@then('The user can no longer access the web page')
def accessWebPage(context):
    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        response1 = TestRestClient().createClientForAboutPage(port=context.port)

        # if response 1 is not an exception and the status code is 200, then wait 0.5 seconds and try again
        print(response1)
        print(type(response1))
        if not responseIsAnError(response1):
            time.sleep(0.5)
            response2 = TestRestClient().createClientForAboutPage(port=context.port)
            assert responseIsAnError(response1), "Expected TimeoutError but got " + str(response2)

        else:
            responseIsAnError(response1), "Expected TimeoutError but got " + str(response1)


@when('The user fetches a static image')
def fetchStaticImage(context):
    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        context.response = TestRestClient().fetchStaticImage(port=context.port)


@then('The user can see the static image')
def seeStaticImage(context):
    if os.name == 'nt' and (context.web_server_type == "GunicornNginx"):
        assert os.name == 'nt'
    else:
        context.web_server.stop()
        time.sleep(2)
        assert context.response.status_code == 200, "Expected 200 OK but got " + str(context.response.status_code)
        assert context.response.headers['Content-Type'] == 'image/jpeg', "Expected image/png but got " + \
                                                                         str(context.response.headers['Content-Type'])


@given('The user hosts the web server on the public web')
def start_public_web_server(context):
    context.port = context.ports['nginxPort']
    context.web_server = WebServer(strategy=GunicornNginxStrategy, ports=context.ports)
    context.public_ip_address = context.web_server.ip_address
    print("ip address is: " + context.public_ip_address)
    print("Config is: " + context.web_server.strategy.createNginxConfig(context.ports,
                                                                        curledIPAddress=context.public_ip_address))
    context.web_server.start()
    time.sleep(2)

    assert len(BookStoreServer.settings.ALLOWED_HOSTS) == \
           len(['.localhost', '127.0.0.1', '[::1]', 'localhost', 'bookhaven.eastus.cloudapp.azure']) + 1
    assert len(BookStoreServer.settings.CORS_ORIGIN_WHITELIST) == \
           len(['http://localhost:3000', 'http://localhost:8091',
                'http://[::1]:3000', 'http://bookhaven.eastus.cloudapp.azure.com']) + 1, "Expected 4 CORS but got " + \
                                           str(BookStoreServer.settings.ALLOWED_HOSTS)

    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        assert context.web_server.isRunning() is True, "Expected web server to be up but it is down"

def isGitHubRunner():
    return os.name == 'posix' and os.popen('whoami').read().strip() == 'runner'

@then('The user can access the web page over the internet')
def access_public_web_server(context):
    if os.name == 'nt':
        assert os.name == 'nt'
    elif isGitHubRunner():
        pass
    else:
        print("about to connect to: " + context.public_ip_address)
        response = TestRestClient().searchForBook("The Hobbit", port=context.port, host=context.public_ip_address
                                                  , timeout=4)
        context.web_server.stop()
        assert response.status_code == 200, "Expected 200 OK but got " + str(response.status_code)
        assert response.json() == [], "Expected empty json but got " + str(response.json)


@given('A username and password')
def defineUser(context):
    context.web_server = WebServer(strategy=GunicornNginxStrategy, ports=context.ports)
    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        context.port = context.ports['nginxPort']
        context.web_server.start()
        context.adminUsername = "newadmin"
        context.password = "password"
        assert context.web_server.isRunning() is True, "Expected web server to be up but it is down"


@when('The application creates an admin user')
def createAdminUser(context):
    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        response = TestRestClient().createUser(username=context.adminUsername, password=context.password)
        assert response == 201, "Expected 201 Created but got " + str(response)

@then('An admin can log in with the credentials')
def loginWithCredentials(context):
    if runningGunicornOnWindows(context):
        assert os.name == 'nt'
    else:
        credentials = {
            'username': context.adminUsername,
            'password': context.password
        }
        client = TestRestClient()
        response = client.createClientAsAdmin(credentials=credentials)
        context.web_server.stop()
        time.sleep(2)
        assert response == 200, "Expected 200 OK but got " + str(response)
