import re

import nginxTemplate
from Source.Interfaces.WebServerStrategy import WebServerStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy

class GunicornNginxStrategy(WebServerStrategy):
    def __init__(self, subprocessLib, osLibrary, ports=None):
        super().__init__(subprocessLib, osLibrary, ports=ports)
        self.gunicorn = GunicornStrategy(subprocessLib, osLibrary, ports=ports)
        if osLibrary.name == 'posix':
            self.inspectedConfigFile = self.createNginxConfig(ports)
            self.nginxConfigFile = '/etc/nginx/sites-available/default'
            self.createConfigFile(self.nginxConfigFile, self.inspectedConfigFile)

    def start(self):
        self.gunicornProcess = self.gunicorn.start()
        if self.osLibrary.name == 'posix':
            print(self.subprocessLib.run(["bash", "ps -efw"], capture_output=True).stdout.decode('utf-8'))
            return self.subprocessLib.Popen(['sudo','nginx', '-g daemon off;'])

    def createStopCommand(self):
        cmd = ''

        if self.osLibrary.name == 'posix':
            cmd = "ps aux | egrep 'BookStoreServer|nginx|runserver' | grep -v 'stopServer.py' " \
                  "| awk '{print $2}' | xargs -r sudo kill -9"

        return cmd

    def isRunning(self):
        if self.osLibrary.name == 'posix':
            cmd2 = "CheckRunGunicorn.sh"
            cmd3 = "CheckRunNginx.sh"
            print(self.subprocessLib.run(["bash", "ps -efw"], capture_output=True).stdout.decode('utf-8'))
            return self.subprocessLib.run(["bash", cmd2], capture_output=True).returncode > 0 and \
                self.subprocessLib.run(["bash", cmd3], capture_output=True).returncode > 0

    def createNginxConfig(self, ports):
        config = re.sub('{nginx_port}', str(ports.get('nginxPort')), nginxTemplate.config)
        config = re.sub('{gunicorn_port}', str(ports.get('gunicornPort')), config)
        config = re.sub('{server_name}', 'BookStore', config)
        path = self.osLibrary.getcwd()
        config = re.sub('{static_path}', path + '/static', config)
        config += '\n'
        return config

    def createConfigFile(self, nginxConfigFile, config):
        try:
            with open(nginxConfigFile, 'w') as nginxFile:
                nginxFile.write(config)
                nginxFile.close()
        except Exception as e:
            print(e)
            print('Error writing to file: ' + nginxConfigFile)
