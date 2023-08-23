import os
import subprocess
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy


class WebServer:
    def __init__(self, strategy=DjangoStrategy, processLibrary=subprocess, osLibrary=os):
        self.strategy = strategy(processLibrary, osLibrary)
        self.processLibrary = processLibrary
        self.process = None
        self.osLibrary = osLibrary

    def start(self):
        if self.strategy.start:
            self.process = self.strategy.start()
        else:
            raise Exception("Unknown web server strategy: " + str(self.strategy))

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.kill()

        cmd = self.strategy.createStopCommand()
        self.executeCommand(cmd)

    def executeCommand(self, cmd):
        try:
            if self.osLibrary.name == 'nt':
                subprocess.run(["powershell", "-Command", cmd], check=True)
            elif self.osLibrary.name == 'posix':
                subprocess.run(["bash", "-c", cmd], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    def isRunning(self):
        return self.strategy.isRunning()

