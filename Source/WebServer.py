import glob
import os
import re
import subprocess
from tempfile import NamedTemporaryFile, gettempdir
from Source.WebServerStrategy.DjangoStrategy import DjangoStrategy


class WebServer:
    def __init__(self, strategy=DjangoStrategy, processLibrary=subprocess, osLibrary=os, ports=None):
        self.processLibrary = processLibrary
        self.process = None
        self.osLibrary = osLibrary
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

        cmd = self.strategy.createStopCommand()
        self.executeCommand(cmd)

    def executeCommand(self, cmd):
        try:
            if self.osLibrary.name == 'nt':
                self.processLibrary.run(["powershell", "-Command", cmd], check=True)
            elif self.osLibrary.name == 'posix':
                self.processLibrary.run(["bash", "-c", cmd], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    def isRunning(self):
        return self.strategy.isRunning()

    def curlIPAddress(self):
        ip_address = self.osLibrary.popen("curl icanhazip.com").read().strip()
        ip_address = re.sub('%20', '', ip_address)
        return ip_address
