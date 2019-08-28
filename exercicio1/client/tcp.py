import socket
import pickle
from datetime import datetime
import pandas as pd


class TCPClient:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.tempo = []
        self.relatorio = None

    def send_op(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(data)
            res = s.recv(1024)
        return pickle.loads(res)

    def run_test(self, loops=10000, armazenar=False):
        temp = []
        data = pickle.dumps({
            'op': 'mult',
            'arg1': 4,
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
