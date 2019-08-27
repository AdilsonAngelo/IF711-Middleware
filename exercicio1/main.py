import server.tcp
from client.tcp import Client
import threading
import matplotlib.pyplot as plt
import time

HOST = '127.0.0.1'
PORT = 6667


if __name__ == "__main__":
    t = threading.Thread(target=server.tcp.start, args=(HOST, PORT))
    t.start()

    time.sleep(1)

    client = Client(HOST, PORT)
    test_result = client.run_test(10000)
    plt.hist(test_result)
    plt.show()
