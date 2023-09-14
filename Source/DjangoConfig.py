

class DjangoConfig:
    @classmethod
    def deleteSqlite(cls):
        import os
        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")

    @classmethod
    def setupMigrations(cls):
        import sys
        import subprocess
        subprocess.Popen([sys.executable, "manage.py", "makemigrations"]).wait()
        subprocess.Popen([sys.executable, "manage.py", "migrate"]).wait()
