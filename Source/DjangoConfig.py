

class DjangoConfig:
    @classmethod
    def delete_sqlite(cls):
        import os
        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")

    @classmethod
    def setup_migrations(cls):
        import sys
        import subprocess
        subprocess.Popen([sys.executable, "manage.py", "makemigrations"]).wait()
        subprocess.Popen([sys.executable, "manage.py", "migrate"]).wait()
