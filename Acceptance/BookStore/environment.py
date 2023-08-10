import os
import signal
import subprocess
import sys
import time

from Acceptance.TestRestClient import TestRestClient
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.WebServer import WebServer


def before_feature(context, feature):
    if "catalog" in feature.name.lower() or "about" in feature.name.lower():
        context.web_server = WebServer()
        context.web_server.start()
        time.sleep(2)


def after_feature(context, feature):
    if "catalog" in feature.name.lower() or "about" in feature.name.lower():
        time.sleep(2)
        context.web_server.stop()
        print("Done")


def before_scenario(context, scenario):
    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()


def clearDatabase():
    SqlBookDatabase().clearCatalog()
