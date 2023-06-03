from Source.Catalog.Catalog import Catalog
from Source.Database.SqlDatabase import SqlDatabase


class PersistentCatalog(Catalog):
    def __init__(self):
        super().__init__(SqlDatabase())
