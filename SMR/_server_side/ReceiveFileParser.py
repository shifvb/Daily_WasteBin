import logging
import time
import json
from .PortAllocator import PortAllocator
import socket
import os


class ReceiveFileParser(object):
    def __init__(self, data, cli_sock, cli_addr):
        self._data = data
        self._cli_sock = cli_sock
        self._cli_addr = cli_addr
        self._logger = logging.getLogger("mylogger")
        self._version = (0, 1)
        self._save_path = "folder"

    def parse(self):
        if self._data['command'] == 'SEND FILE':
            client_version = tuple([int(_) for _ in self._data['version'].split(".")])
            if self._version < client_version:
                self._logger.warning("client version too high! v{}.{} < v{}.{}".format(*self._version, *client_version))
            _parse_command_func = getattr(self, "_parse_command_v{}_{}".format(*client_version),
                                          lambda *args: self._logger.error("version not supported! {}"))
            _parse_command_func()

    def _parse_command_v0_1(self):
        pa = PortAllocator()
        file_receive_port = pa.get_port()
        try:
            self._cli_sock.send(json.dumps({
                "version": "0.1",
                "type": self._data["command"] + " RESP",
                "allocate_port": file_receive_port
            }).encode('utf-8'))
            self._save(file_receive_port)
        finally:
            pa.release_port(file_receive_port)
            self._cli_sock.close()

    def _save(self, cli_port):
        s = socket.socket()
        s.bind(("0.0.0.0", cli_port))
        s.listen(1)
        _fr_sock, _ = s.accept()

        if not (os.path.exists(self._save_path) and os.path.isdir(self._save_path)):
            os.mkdir(self._save_path)
        with open(os.path.join(self._save_path, self._data['filename']), 'wb') as f:
            while True:
                _buf = _fr_sock.recv(4096)
                if _buf == b'':
                    break
                f.write(_buf)
