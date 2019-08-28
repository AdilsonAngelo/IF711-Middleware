import socket
import threading
import pickle
from calculator import ops

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
                    res = {'ERRO': 'Operação não encontrada'}
                conn.sendall(pickle.dumps(res))
    finally:
        conn.close()


def start(host, port):
    print(f'Iniciando servidor em {host}:{port}')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(100)
        while True:
            # Aguardando conexão
            conn, add = s.accept()
            # Dispara worker
            t = threading.Thread(target=client_worker, args=(conn,))
            t.start()
    finally:
        s.close()
