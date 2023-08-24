from Source.Interfaces.WebServerStrategy import WebServerStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy


class GunicornNginxStrategy(WebServerStrategy):
    def __init__(self, subprocessLib, osLibrary):
        super().__init__(subprocessLib, osLibrary)
        self.gunicorn = GunicornStrategy(subprocessLib, osLibrary)

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
