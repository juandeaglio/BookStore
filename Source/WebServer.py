import os
import subprocess
import sys


class WebServer:
    def __init__(self, strategy="Django", processLibrary=subprocess, osLibrary=os):
        self.strategy = strategy
        self.processLibrary = processLibrary
        self.process = None
        self.running = False
        self.osLibrary = osLibrary

    def start(self):
        if self.strategy == "Django":
            self.process = self.processLibrary.Popen([sys.executable, "startDjangoWithTestUser.py"])
        else:
            raise Exception("Unknown web server strategy: " + self.strategy)
        self.running = True

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.kill()

        cmd = ""
        if self.osLibrary.name == 'nt':
            cmd = "Get-WmiObject Win32_Process | Where-Object " \
                  "{ $_.Name -match 'python' -and $_.CommandLine -like '*runserver*' } | " \
                  "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
        elif os.name == 'posix':
            cmd = "ps aux | grep 'python' | grep 'runserver' | awk '{print $2}' | xargs kill -9"

        # Try to run the command and catch any errors
        try:
            if os.name == 'nt':
                subprocess.run(["powershell", "-Command", cmd], check=True)
            elif os.name == 'posix':
                subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

        self.running = False

    def isRunning(self):
        return self.running


