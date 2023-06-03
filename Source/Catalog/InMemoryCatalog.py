from Source.Catalog.Catalog import Catalog
from Source.Database.InMemoryDatabase import InMemoryDatabase


class InMemoryCatalog(Catalog):
    def __init__(self):
        super().__init__(InMemoryDatabase())
