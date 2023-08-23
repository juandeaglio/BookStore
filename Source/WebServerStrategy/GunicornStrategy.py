import os

from Source.Interfaces.WebServerStrategy import WebServerStrategy


class GunicornStrategy(WebServerStrategy):
    def start(self, processLibrary):
        if os.name == 'posix':
            return processLibrary.Popen(["gunicorn", "-b", "0.0.0.0:8091", "BookStoreServer.wsgi"])

    def createStopCommand(self):
        pass

    def isRunning(self, subprocessLib):
        pass
