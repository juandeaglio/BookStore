from Source.Catalog.Catalog import Catalog
from Source.Database.SqlInMemoryBooks import SqlInMemoryBooks


class PersistentCatalog(Catalog):
    def __init__(self):
        super().__init__(SqlInMemoryBooks())
