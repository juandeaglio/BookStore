import time

from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.DjangoConfig import DjangoConfig
from Source.WebServer import WebServer


def before_scenario(context, scenario):
    context.ports = {'nginxPort': 8091, 'gunicornPort': 8092}
    clear_database()
    DjangoConfig.setup_migrations()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()
    context.web_server = WebServer(ports=context.ports)
    if "web server" not in scenario.name.lower():
        context.web_server.start()
        time.sleep(4)



def after_scenario(context, scenario):
    context.web_server.stop()
    time.sleep(2)


def after_all(context):
    context.ports = {'nginxPort': 8091, 'gunicornPort': 8092}
    web_server = WebServer(ports=context.ports)
    web_server.stop()


def clear_database():
    SqlBookDatabase().clear_catalog()
    DjangoConfig.delete_sqlite()


