import server.tcp
import server.udp
from client.tcp import TCPClient
from client.udp import UDPClient
import threading
import click
import matplotlib.pyplot as plt
import pandas as pd


@click.group()
def cli():
    pass


@click.command()
@click.option('--host', '-h', default='127.0.0.1', help='hostname')
@click.option('--port', '-p', default=6666, help='porta')
@click.option('--clients', '-c', default=1, help='numero de clientes', type=click.IntRange(1, 5))
@click.option('--tcp/--udp', default=True)
def teste(host, port, clients, tcp):
    if tcp:
        SERVER = server.tcp.start
        CLIENT = TCPClient
    else:
        SERVER = server.udp.start
        CLIENT = UDPClient

    threading.Thread(target=SERVER, args=(host, port)).start()

    cs = [CLIENT(host, port) for i in range(clients)]

    t0 = threading.Thread(target=cs[0].run_test, kwargs={'armazenar': True})

    client_threads = [t0]
    t0.start()

    for i in range(clients - 1):
        client_threads.append(threading.Thread(target=cs[i + 1].run_test))
        client_threads[-1].start()

    for i in range(clients):
        client_threads[i].join()

    print(cs[0].relatorio)

    with open(f'_saida/log/_{"tcp" if tcp else "udp"}{clients}.log', 'w') as log_file:
        log_file.write(str(cs[0].relatorio))

    with open(f'_saida/csv/_{"tcp" if tcp else "udp"}{clients}.csv', 'w') as csv_file:
        csv_file.write('microsegundos\n')
        for res in cs[0].tempo:
            csv_file.write(f'{res}\n')


@click.command()
def graficos():
    tipo = []
    media = []
    clientes = []
    for i in range(5):
        tipo.append('tcp')
        media.append(pd.read_csv(
            f'_saida/csv/_tcp{i+1}.csv').microsegundos.mean())
        clientes.append(i + 1)
        tipo.append('udp')
        media.append(pd.read_csv(
            f'_saida/csv/_udp{i+1}.csv').microsegundos.mean())
        clientes.append(i + 1)

    df = pd.DataFrame()
    df['tipo'] = pd.Series(tipo)
    df['media'] = pd.Series(media)
    df['clientes'] = pd.Series(clientes)

    agg = df.groupby(['tipo', 'clientes'])['media'].aggregate(sum).unstack()
    agg.plot(kind='bar')
    plt.ylabel('Tempo médio (microsegundos)')
    plt.xlabel('Tipo Socket')

    plt.savefig('_saida/png/barplot.png')


cli.add_command(teste)
cli.add_command(graficos)

if __name__ == "__main__":
    cli()
