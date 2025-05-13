# client_concorrente.py
from client import Client
import threading

SERVER_PORTS = [5001, 5002]
SEQUENCER_PORT = 6001

def cliente_A():
    client = Client(1, SERVER_PORTS, SEQUENCER_PORT)
    client.execute_transaction([
        {"type": "read", "item": "x", "delay": 1},
        {"type": "write", "item": "x", "value": 100},
    ])

def cliente_B():
    client = Client(2, SERVER_PORTS, SEQUENCER_PORT)
    client.execute_transaction([
        {"type": "read", "item": "x", "delay": 1},
        {"type": "write", "item": "x", "value": 200},
    ])

# Executar em paralelo
threading.Thread(target=cliente_A).start()
threading.Thread(target=cliente_B).start()


# simula dois clientes concorrendo para modificar o mesmo item (x) ao mesmo tempo.