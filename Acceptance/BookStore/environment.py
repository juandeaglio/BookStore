import os
import signal
import subprocess
import sys
import time

from Acceptance.TestRestClient import TestRestClient
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlDatabase import SqlDatabase


def before_all(context):
    startDjangoServer(context)
    time.sleep(1)


def startDjangoServer(context):
    print(str(os.getcwd()))
    context.process = subprocess.Popen([sys.executable, "startDjangoWithTestUser.py"])


def before_scenario(context, scenario):
    clearDatabase()
    context.defaultPort = 8091
    context.catalog = PersistentCatalog()


def stopDjangoServer(context):
    if context.process:
        context.process.terminate()
        context.process.kill()

    cmd = "Get-WmiObject Win32_Process | Where-Object " \
          "{ $_.Name -match 'python' -and $_.CommandLine -like '*runserver*' } | " \
          "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"

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
