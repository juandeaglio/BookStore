import os
import subprocess

if __name__ == '__main__':
    os.environ['TESTPW'] = 'creativepassword'
    os.environ['TESTUSERNAME'] = 'username'
    os.environ['ENVIRONMENT'] = 'test'
    import os

    # define the directory path
    dir_path = './venv/Scripts/'

    # check if the directory exists
    if os.path.exists(dir_path) and os.path.isfile(dir_path+"python.exe"):
        p = subprocess.call("./venv/Scripts/python manage.py runserver 8091 --noreload "
                            "--settings catalog_service.settings_development")
    else:
        p = subprocess.call("python manage.py runserver 8091 --noreload "
                            "--settings catalog_service.settings_development")
