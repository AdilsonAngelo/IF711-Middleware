import socket
import pickle
from datetime import datetime
import numpy as np

HOST = '127.0.0.1'
PORT = 6666
OPS = ['add', 'sub', 'mult', 'div']


class Client:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.tempo = []

    def send_op(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(data)
            res = s.recv(1024)
        print(pickle.loads(res))
        return pickle.loads(res)

    def run_test(self, loops=10000):
        self.tempo = []
        data = pickle.dumps({
            'op': 'mult',
            'arg1': 4,
            'arg2': 8
        })
        for i in range(loops):
            antes = datetime.now()
            self.send_op(data)
            delta = datetime.now() - antes

            self.tempo.append(int(delta.total_seconds() * 1e6))
        return self.tempo
