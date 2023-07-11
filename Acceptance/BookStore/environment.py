import os, subprocess
import time

from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlDatabase import SqlDatabase


def startDjangoServer():
    subprocess.Popen("./venv/Scripts/python.exe manage.py runserver 8091")


def before_scenario(context, scenario):
    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()
    startDjangoServer()
    time.sleep(1)


def stopDjangoServer():
    subprocess.Popen('Get-Process -Name python | Stop-Process -Force')


def after_feature(context, scenario):
    stopDjangoServer()


def after_scenario(context, scenario):
    time.sleep(1)
    stopDjangoServer()


def clearDatabase():
    SqlDatabase().clearData()
