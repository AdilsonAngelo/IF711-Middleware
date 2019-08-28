import socket
import pickle
from calculator import ops

HASH_OPS = {
    'add': ops.add,
    'sub': ops.sub,
    'mult': ops.mult,
    'div': ops.div
}


def start(host, port):
    print(f'Iniciando servidor em {host}:{port}')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind((host, port))

        while True:
            # Aguardando conexão
            data, address = s.recvfrom(4096)
            if data:
                op = pickle.loads(data)
                if op['op'].lower() in HASH_OPS:
                    res = {'res': HASH_OPS[op['op']](op['arg1'], op['arg2'])}
                else:
                    res = {'ERRO': 'Operação não encontrada'}
                sent = s.sendto(pickle.dumps(res), address)
    finally:
        s.close()
