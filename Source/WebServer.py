import os
import subprocess
import sys


class WebServer:
    def __init__(self, strategy="Django", processLibrary=subprocess, osLibrary=os):
        self.strategy = strategy
        self.processLibrary = processLibrary
        self.process = None
        self.osLibrary = osLibrary
        self.type = strategy

    def start(self):
        if self.strategy == "Django":
            self.process = self.processLibrary.Popen([sys.executable, "startDjangoWithTestUser.py"])
        elif self.strategy == "gunicorn":
            if os.name == 'posix':
                self.process = self.processLibrary.Popen(["gunicorn", "BookStoreServer.wsgi"])
        else:
            raise Exception("Unknown web server strategy: " + self.strategy)

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
                subprocess.run(cmd, shell=True, check=True)

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
                cmd = "ps aux | grep 'python' | grep 'runserver' | awk '{print $2}' | xargs -r kill -9"
            elif self.type == "gunicorn":
                cmd = "ps aux | grep 'gunicorn' | grep 'BookStoreServer' | awk '{print $2}' | xargs -r kill -9"
        return cmd

    def isRunning(self):
        cmd = ''
        if os.name == 'nt':
            if self.type == "Django":
                #get all python processes and filter out the ones that are not runserver, count the number of processes and return true if there is at least one
                cmd = "CheckRunServerDjango.ps1"
            print(subprocess.run(["powershell", "-File", cmd], capture_output=True).returncode)
            return subprocess.run(["powershell", "-File", cmd], capture_output=True).returncode > 0

        elif os.name == 'posix':
            cmd = "CheckRunServer.sh"
            return subprocess.run(["bash", cmd], capture_output=True).returncode > 0
