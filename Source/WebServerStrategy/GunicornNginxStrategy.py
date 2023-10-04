import re

from Source.WebServerStrategy import nginx_template
from Source.Interfaces.WebServerStrategy import WebServerStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy


class GunicornNginxStrategy(WebServerStrategy):
    def __init__(self, sub_process_library, os_library, ports=None):
        super().__init__(sub_process_library, os_library, ports=ports)
        self.gunicorn = GunicornStrategy(sub_process_library, os_library, ports=ports)
        if os_library.name == 'posix':
            self.inspected_config_file = self.create_nginx_config(ports)
            self.nginx_config_file = './nginx.conf'
            self.create_config_file(self.nginx_config_file, self.inspected_config_file)

    def start(self):
        self.gunicorn_process = self.gunicorn.start()
        if self.os_library.name == 'posix':
            print(self.sub_process_lib.run(["bash", "ps -efw"], capture_output=True).stdout.decode('utf-8'))
            return self.sub_process_lib.Popen(['sudo', 'nginx', '-g daemon off;'])

    def create_stop_command(self):
        cmd = ''

        if self.os_library.name == 'posix':
            cmd = "ps aux | egrep 'BookStoreServer|nginx|runserver' | grep -v 'stopServer.py' | grep -v 'grep'" \
                  "| awk '{print $2}' | xargs -r sudo kill -9"

        return cmd

    def is_running(self):
        if self.os_library.name == 'posix':
            cmd2 = "./Source/Scripts/CheckRunGunicorn.sh"
            cmd3 = "./Source/Scripts/CheckRunNginx.sh"
            return self.sub_process_lib.run(["bash", cmd2], capture_output=True).returncode > 0 and \
                   self.sub_process_lib.run(["bash", cmd3], capture_output=True).returncode > 0

    def create_nginx_config(self, ports, curled_ip_address='localhost'):
        nginx_port = ports.get('nginx_port') or 80
        gunicorn_port = ports.get('gunicorn_port') or 8091
        config = re.sub('{nginx_port}', str(nginx_port), nginx_template.config)
        config = re.sub('{gunicorn_port}', str(gunicorn_port), config)
        config = re.sub('{server_name}', 'BookStore', config)
        config = re.sub('{static_path}', '/var/www/static', config)
        config = re.sub('{my_ip_address}', curled_ip_address, config)
        config += '\n'
        return config

    def create_config_file(self, nginx_config_file, config):
        try:
            with open(nginx_config_file, 'w') as nginx_file:
                nginx_file.write(config)
                nginx_file.close()
        except Exception as e:
            print(e)
            print('Error writing to file: ' + nginx_config_file)
