import socket
import threading
import pickle
from calculator import ops

from pprint import pprint

HOST = '127.0.0.1'
PORT = 6666

HASH_OPS = {
    'add': ops.add,
    'sub': ops.sub,
    'mult': ops.mult,
    'div': ops.div
}


def client_worker(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                op = pickle.loads(data)
                if op['op'].lower() in HASH_OPS:
                    res = {'res': HASH_OPS[op['op']](op['arg1'], op['arg2'])}
                else:
                    res = {'res': 'Operação não encontrada'}
                conn.sendall(pickle.dumps(res))
    except Exception as e:
        conn.close()
        raise e


def start(host=HOST, port=PORT):
    print(f'Iniciando servidor em {host}:{port}')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(100)
        while True:
            # print('Aguardando conexão...')
            conn, add = s.accept()
            # print(f'Conectado com: {add[0]}:{add[1]}')
            t = threading.Thread(target=client_worker, args=(conn,))
            t.start()
    except Exception as e:
        s.close()
        raise e
