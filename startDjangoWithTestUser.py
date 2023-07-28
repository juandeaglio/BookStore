import os
import subprocess

if __name__ == '__main__':
    os.environ['TESTPW'] = 'creativepassword'
    os.environ['TESTUSERNAME'] = 'username'
    os.environ['ENVIRONMENT'] = 'test'
    p = subprocess.call("./venv/Scripts/python.exe manage.py runserver 8091 --noreload "
                        "--settings catalog_service.settings_development")
