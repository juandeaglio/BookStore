from abc import ABC, abstractmethod


class WebServerStrategy(ABC):
    def __init__(self, subprocessLib, osLibrary, ports=None):
        self.subprocessLib = subprocessLib
        self.osLibrary = osLibrary
        self.ports = ports or {}

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def createStopCommand(self):
        pass

    @abstractmethod
    def isRunning(self):
        pass
