from Source.Interfaces.WebServerStrategy import WebServerStrategy


class GunicornNginxStrategy(WebServerStrategy):
    def start(self, processLibrary):
        pass

    def createStopCommand(self):
        pass

    def isRunning(self, subprocessLib):
        pass
