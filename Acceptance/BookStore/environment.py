import time

from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.WebServer import WebServer


def before_scenario(context, scenario):
    context.ports = {'nginxPort': 8091, 'gunicornPort': 8092}
    context.web_server = WebServer(ports=context.ports)
    if "web server" not in scenario.name.lower():
        context.web_server.start()
        time.sleep(1)

    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()


def after_scenario(context, scenario):
    context.web_server.stop()
    time.sleep(1)


def clearDatabase():
    SqlBookDatabase().clearCatalog()
