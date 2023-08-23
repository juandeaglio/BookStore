from abc import ABC, abstractmethod


class WebServerStrategy(ABC):
    @abstractmethod
    def start(self, processLibrary):
        pass

    @abstractmethod
    def createStopCommand(self):
        pass

    @abstractmethod
    def isRunning(self, subprocessLib):
        pass
