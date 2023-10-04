from Source.Interfaces.WebServerStrategy import WebServerStrategy


class GunicornStrategy(WebServerStrategy):
    def __init__(self, sub_process_library, os_library, ports=None):
        super().__init__(sub_process_library, os_library, ports=ports)

    def start(self):
        port = 8091
        if self.ports.get('gunicornPort'):
            port = self.ports.get('gunicornPort')

        if self.os_library.name == 'posix':
            return self.sub_process_lib.Popen(["gunicorn", "-b", "0.0.0.0:" + str(port), "BookStoreServer.wsgi"])

    def create_stop_command(self):
        cmd = ''

        if self.os_library.name == 'posix':
            cmd = "ps aux | grep 'gunicorn' | grep 'BookStoreServer' | grep -v 'stopServer.py'  | awk '{print $2}' " \
                  "| xargs -r kill -9"

        return cmd

    def is_running(self):
        if self.os_library.name == 'posix':
            cmd2 = "./Source/Scripts/CheckRunGunicorn.sh"
            return self.sub_process_lib.run(["bash", cmd2], capture_output=True).returncode > 0
