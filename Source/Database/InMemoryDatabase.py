from Source.Interfaces.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def synchronize(self, books):
        return books
