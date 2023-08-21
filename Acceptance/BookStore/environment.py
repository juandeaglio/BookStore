import time

from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.WebServer import WebServer


def before_scenario(context, scenario):
    context.web_server = WebServer()
    if "web server" not in scenario.name.lower():
        context.web_server.start()
        time.sleep(4)

    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()


def after_scenario(context, scenario):
    time.sleep(4)
    context.web_server.stop()
    print("Done")


def clearDatabase():
    SqlBookDatabase().clearCatalog()
