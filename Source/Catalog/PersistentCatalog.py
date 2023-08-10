from Source.Catalog.Catalog import Catalog
from Source.Database.SqlBookDatabase import SqlBookDatabase


class PersistentCatalog(Catalog):
    def __init__(self):
        super().__init__(SqlBookDatabase())
