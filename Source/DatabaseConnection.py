from abc import ABC, abstractmethod


class DatabaseConnection(ABC):
    @abstractmethod
    def insert(self, books):
        pass

    @abstractmethod
    def selectAll(self):
        pass

    @abstractmethod
    def delete(self, entry):
        pass

    @abstractmethod
    def select(self, book):
        pass