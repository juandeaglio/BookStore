import os
import subprocess
import sys

if __name__ == '__main__':
    os.environ['TESTPW'] = 'creativepassword'
    os.environ['TESTUSERNAME'] = 'username'
    os.environ['ENVIRONMENT'] = 'test'

    # define the directory path
    dir_path = './venv/Scripts/'

    p = subprocess.call(sys.executable + " manage.py runserver 8091 --noreload "
                            "--settings catalog_service.settings_development")
