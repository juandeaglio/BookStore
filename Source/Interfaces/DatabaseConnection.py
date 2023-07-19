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

    def delete(self, entry):
        pass

    def deleteWhereTitle(self, title):
        pass

    @abstractmethod
    def selectWith(self, bookDetail):
        pass
