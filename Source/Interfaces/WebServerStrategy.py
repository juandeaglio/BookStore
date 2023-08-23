from abc import ABC, abstractmethod


class WebServerStrategy(ABC):
    def __init__(self, subprocessLib, osLibrary):
        self.subprocessLib = subprocessLib
        self.osLibrary = osLibrary

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def createStopCommand(self):
        pass

    @abstractmethod
    def isRunning(self):
        pass
