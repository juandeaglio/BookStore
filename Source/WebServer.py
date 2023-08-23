import os
import subprocess
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy


class WebServer:
    def __init__(self, strategy=DjangoStrategy, processLibrary=subprocess, osLibrary=os):
        self.strategy = strategy()
        self.processLibrary = processLibrary
        self.process = None
        self.osLibrary = osLibrary
        self.type = strategy

    def start(self):
        if self.strategy.start:
            self.process = self.strategy.start(self.processLibrary)
        else:
            raise Exception("Unknown web server strategy: " + str(self.strategy))

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.kill()

        cmd = self.createStopCommand()

        self.executeCommand(cmd)

    def executeCommand(self, cmd):
        try:
            if os.name == 'nt':
                subprocess.run(["powershell", "-Command", cmd], check=True)
            elif os.name == 'posix':
                subprocess.run(["bash", "-c", cmd], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    def createStopCommand(self):
        cmd = ""

        if self.osLibrary.name == 'nt':
            if self.type == "Django":
                cmd = "Get-WmiObject Win32_Process | Where-Object " \
                      "{ $_.Name -match 'python' -and $_.CommandLine -like '*runserver*' } | " \
                      "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
        elif os.name == 'posix':
            if self.type =="Django":
                cmd = "ps aux | grep 'python' | grep 'runserver' | grep -v 'kill' | awk '{print $2}' | xargs -r kill -9"
            elif self.type == "gunicorn":
                cmd = "ps aux | grep 'gunicorn' | grep 'BookStoreServer' | grep -v 'stopServer.py'  | awk '{print $2}' | xargs -r kill -9"
        return cmd

    def isRunning(self):
        return self.strategy.isRunning(self.processLibrary)

