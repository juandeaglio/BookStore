import os
import signal
import subprocess
import time

from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlDatabase import SqlDatabase


def startDjangoServer(context):
    context.p = subprocess.Popen("./venv/Scripts/python.exe startDjangoWithTestUser.py")


def before_scenario(context, scenario):
    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()
    startDjangoServer(context)


def stopDjangoServer(context):
    if context.p:
        context.p.terminate()
        context.p.kill()
        os.kill(context.p.pid, signal.CTRL_C_EVENT)
        del context.p


def after_feature(context, scenario):
    pass


def after_scenario(context, scenario):
    time.sleep(1)
    stopDjangoServer(context)


def clearDatabase():
    SqlDatabase().clearData()
