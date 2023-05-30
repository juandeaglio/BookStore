from Source.Catalog.Catalog import CatalogInterface
from Source.Database.SqlDatabase import SqlDatabase


class PersistentCatalog(CatalogInterface):
    def __init__(self):
        dbConnection = SqlDatabase()
        super().__init__(dbConnection)
