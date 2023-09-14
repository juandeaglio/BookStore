class DjangoConfig:
    @classmethod
    def deleteSqlite(cls):
        import os
        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")

    @classmethod
    def setupMigrations(cls):
        import os
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")