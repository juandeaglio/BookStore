from abc import ABC, abstractmethod


class SocketService(ABC):
    @abstractmethod
    def __init__(self):
        self.connections = 0

    @abstractmethod
    def serve(self, socket):
        self.connections += 1

