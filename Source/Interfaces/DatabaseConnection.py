from abc import ABC, abstractmethod


class DatabaseConnection(ABC):
    @abstractmethod
    def insertBooksIntoCatalogTable(self, books):
        pass

    @abstractmethod
    def selectAll(self):
        pass

    @abstractmethod
    def select(self, book):
        pass

    @abstractmethod
    def delete(self, entry):
        pass

    @abstractmethod
    def deleteWhereTitle(self, title):
        pass

    @abstractmethod
    def selectWith(self, bookDetail):
        pass
