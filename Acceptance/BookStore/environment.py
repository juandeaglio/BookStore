import os
import signal
import subprocess
import time

from Acceptance.TestRestClient import TestRestClient
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlDatabase import SqlDatabase


def before_all(context):
    startDjangoServer(context)


def startDjangoServer(context):
    print(str(os.getcwd()))
    context.process = subprocess.Popen("python.exe startDjangoWithTestUser.py")


def before_scenario(context, scenario):
    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()


def stopDjangoServer(context):
    if context.process:
        context.process.terminate()
        context.process.kill()

    cmd = "Get-WmiObject Win32_Process -Filter \"name = 'python.exe'\" | Where-Object { $_.CommandLine -like '*runserver*' } | ForEach-Object { Stop-Process -Id $_.ProcessId }"

    # Try to run the command and catch any errors
    try:
        subprocess.run(["powershell", "-Command", cmd], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")


def after_all(context):
    time.sleep(2)
    stopDjangoServer(context)
    print("Done")


def clearDatabase():
    SqlDatabase().clearData()
