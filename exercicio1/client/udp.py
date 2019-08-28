import socket
from datetime import datetime
import pickle
import pandas as pd


class UDPClient:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.tempo = []
        self.relatorio = None

    def send_op(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sent = sock.sendto(data, (self.HOST, self.PORT))
            res, server = sock.recvfrom(1024)
            return pickle.loads(res)
        finally:
            sock.close()

    def run_test(self, loops=10000, armazenar=False):
        temp = []
        data = pickle.dumps({
            'op': 'mult',
            'arg1': 5,
            'arg2': 8
        })

        if armazenar:
            print(f'Iniciando teste com {loops} iterações...')
            for i in range(loops):
                antes = datetime.now()
                self.send_op(data)
                delta = datetime.now() - antes
                temp.append(int(delta.total_seconds() * 1e6))
            print('Teste finalizado com sucesso!\n')
            self.tempo = pd.Series(temp)
            self.relatorio = self.tempo.describe()
            return self.tempo
        else:
            for i in range(loops):
                self.send_op(data)
            return
