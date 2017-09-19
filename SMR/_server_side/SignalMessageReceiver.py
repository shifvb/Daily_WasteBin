import socket
import json
import logging
import sys


class SignalMessageReceiver(object):
    """A single thread message receiver"""

    def __init__(self, port=32947, debug=False):
        self._listen_port = port
        self._init_logger(debug)

    def listen(self, parsers):
        """start handling requests"""
        _sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        _sock.bind(("0.0.0.0", self._listen_port))
        _sock.listen(1)
        while True:
            cli_sock, cli_addr = _sock.accept()
            _data = str()
            while True:
                _buf = cli_sock.recv(4096).decode("utf-8")
                if _buf == "":
                    break
                _data += _buf
            json_data = json.loads(_data)
            self._logger.debug(json_data)
            for parser in parsers:
                parser(json_data, cli_sock, cli_addr).parse()

    def _init_logger(self, debug):
        self._logger = logging.getLogger("mylogger")
        _level = logging.DEBUG if debug else logging.INFO
        _handler = logging.StreamHandler(sys.stdout)
        _handler.setLevel(logging.DEBUG)
        self._logger.addHandler(_handler)
        self._logger.setLevel(_level)
