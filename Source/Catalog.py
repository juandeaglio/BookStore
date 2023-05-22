from Source.CatalogInterface import CatalogInterface
from Source.SqlDatabase import SqlDatabase


class Catalog(CatalogInterface):
    def __init__(self):
        dbConnection = SqlDatabase()
        super().__init__(dbConnection)
