from Source.Catalog.Catalog import CatalogInterface
from Source.Database.InMemoryDatabase import InMemoryDatabase


class InMemoryCatalog(CatalogInterface):
    def __init__(self):
        dbConnection = InMemoryDatabase()
        super().__init__(dbConnection)
