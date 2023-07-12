import os, subprocess
import time

from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlDatabase import SqlDatabase


def startDjangoServer(context):
    context.p = subprocess.Popen("./venv/Scripts/python.exe manage.py runserver 8091")


def before_scenario(context, scenario):
    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()
    startDjangoServer(context)
    time.sleep(1)


def stopDjangoServer(context):
    if context.p and context.p.poll:
        context.p.terminate()


def after_feature(context, scenario):
    stopDjangoServer(context)


def after_scenario(context, scenario):
    time.sleep(1)
    stopDjangoServer(context)


def clearDatabase():
    SqlDatabase().clearData()
