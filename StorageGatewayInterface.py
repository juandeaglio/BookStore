from abc import ABC, abstractmethod


class StorageGatewayInterface(ABC):
    @abstractmethod
    def save(self, books):
        pass

    @abstractmethod
    def load(self):
        pass
