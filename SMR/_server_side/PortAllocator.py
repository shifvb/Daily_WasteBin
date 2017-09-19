import threading
import random
import socket


class PortAllocator(object):
    """
    (thread-safe) An unused port generator. If haven't got an unused port after max_try_times, it returns 0.
    usage:
        pa = PortAllocator(start_port=45678, end_port=45697, max_try_times=100)
        port = pa.get_port()
        try:
            # do something
        except:
            # deal with it...
        finally:
            pa.release_port()
    """
    _lock = threading.Lock()
    _allocated_ports = []

    def __init__(self, start_port=256, end_port=65536, max_try_times=100, allocate_ip="127.0.0.1"):
        """
        :param start_port: Allocated port equals or more than start_port. default to 25665536
        :param end_port: Allocated port less than end_port. default to 256
        :param max_try_times: Max try times when allocating port. default to 100
        :param allocate_ip: The ip allocated from, default is "127.0.0.1"
        """
        self._start_port = start_port
        self._end_port = end_port
        self._max_try_times = max_try_times
        self._try_times = 0
        self._allocate_ip = allocate_ip

    def get_port(self) -> int:
        """
        get an unused port
        :return: an unused port
        """
        self._lock.acquire()
        while self._try_times < self._max_try_times:
            _port_to_try = random.choice(range(self._start_port, self._end_port))
            if _port_to_try in self._allocated_ports or self._is_open(self._allocate_ip, _port_to_try):
                self._try_times += 1
            else:
                self._allocated_ports.append(_port_to_try)
                _port = _port_to_try
                break
        else:
            _port = 0
        self._lock.release()
        return _port

    def release_port(self, port: int):
        """
        Release your used port. The reason why should release the used port
        is that the PortAllocator keeps tracking allocated ports.
        :param port: used port
        """
        self._lock.acquire()
        self._allocated_ports.remove(port)
        self._lock.release()

    @staticmethod
    def _is_open(ip, port):
        try:
            _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _sock.connect((ip, port))
            _sock.shutdown(2)
            return True
        except:
            return False
