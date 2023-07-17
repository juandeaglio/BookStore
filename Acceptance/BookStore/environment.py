import os
import signal
import subprocess
import sys
import time

from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlDatabase import SqlDatabase


def before_all(context):
    startDjangoServer(context)

def startDjangoServer(context):
    context.process = subprocess.Popen("./venv/Scripts/python.exe startDjangoWithTestUser.py")


def before_scenario(context, scenario):
    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()


def stopDjangoServer(context):
    if context.process:
        context.process.terminate()
        context.process.kill()

def after_scenario(context, scenario):
    time.sleep(1)


def after_all(context):
    stopDjangoServer(context)
    os.kill(context.process.pid, signal.CTRL_C_EVENT)
    print("Done")


def clearDatabase():
    SqlDatabase().clearData()
