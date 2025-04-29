# client2.py
from client import Client
import time

SERVER_PORTS = [5001, 5002]
SEQUENCER_PORT = 6001

# Cliente 2: Lê versão obsoleta (0) e tenta escrever
client = Client(2, SERVER_PORTS, SEQUENCER_PORT)

# Passo 1: Ler x (versão 0) antes do client1 commitar
client.execute_transaction([
    {"type": "read", "item": "x", "delay": 1},
    {"type": "write", "item": "x", "value": 20, "delay": 2},
])

# Passo 2: Garantir que o client1 já commtou antes do client2 enviar o commit
time.sleep(5)  # Aguardar o client1 completar
client.send_commit()