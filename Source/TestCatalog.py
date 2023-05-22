from Source.CatalogInterface import CatalogInterface
from Source.InMemoryDatabase import InMemoryDatabase


class TestCatalog(CatalogInterface):
    def __init__(self):
        dbConnection = InMemoryDatabase()
        super().__init__(dbConnection)
