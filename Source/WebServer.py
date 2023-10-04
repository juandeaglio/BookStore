import glob
import os
import re
import subprocess
from tempfile import NamedTemporaryFile, gettempdir
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy


class WebServer:
    def __init__(self, strategy=DjangoStrategy, processLibrary=subprocess, osLibrary=os, ports=None):
        self.process_library = processLibrary
        self.process = None
        self.os_library = osLibrary
        self.ports = ports or {}
        self.strategy = strategy(processLibrary, osLibrary, ports=self.ports)
        self.temp_ip_address_file = self.fetch_cached_ip()

        if self.fetch_cached_ip():
            with open(self.temp_ip_address_file[0]) as f:
                self.ip_address = f.read()
        else:
            self.ip_address = self.curlIPAddress()
            with NamedTemporaryFile(prefix="ip_address", mode='w', delete=False) as f:
                f.write(self.ip_address)
                f.close()

    def fetch_cached_ip(self):
        temp_dir = gettempdir()
        return glob.glob(f'{temp_dir}/ip_address*')

    def start(self):
        if self.strategy.start:
            self.process = self.strategy.start()
        else:
            raise Exception("Unknown web server strategy: " + str(self.strategy))

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.kill()

        cmd = self.strategy.create_stop_command()
        self.execute_command(cmd)

    def execute_command(self, cmd):
        try:
            if self.os_library.name == 'nt':
                self.process_library.run(["powershell", "-Command", cmd], check=True)
            elif self.os_library.name == 'posix':
                self.process_library.run(["bash", "-c", cmd], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    def is_running(self):
        return self.strategy.is_running()

    def curlIPAddress(self):
        ip_address = self.os_library.popen("curl icanhazip.com").read().strip()
        ip_address = re.sub('%20', '', ip_address)
        return ip_address
