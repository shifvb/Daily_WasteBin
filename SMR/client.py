import socket
import time
import uuid
import json
import os


def main():
    server_ip = "192.168.1.101"
    file_path = r"D:\CloudMusic\[.que] - Drops.mp3"

    sock = socket.socket()
    sock.connect((server_ip, 32947))
    sock.send(json.dumps({
        "version": "0.1",
        "command": "SEND FILE",
        "filename": os.path.split(file_path)[1],
    }).encode())
    sock.shutdown(socket.SHUT_WR)
    data = json.loads(sock.recv(4096))
    print(data)
    sock.close()

    sock = socket.socket()
    sock.connect((server_ip, data['allocate_port']))
    with open(file_path, 'rb') as f:
        for data in f:
            sock.send(data)
        sock.close()


if __name__ == '__main__':
    main()
