from abc import ABC, abstractmethod


class SocketService(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def serve(self, socket):
        pass
