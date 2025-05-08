# client1.py
from client import Client

# Configurações
SERVER_PORTS = [5001, 5002]  # Portas dos servidores
SEQUENCER_PORT = 6001        # Porta do sequenciador

# Cliente 1: Atualiza x para 15
client = Client(1, SERVER_PORTS, SEQUENCER_PORT)
client.execute_transaction([
    {"type": "read", "item": "x", "delay": 1},
    {"type": "write", "item": "x", "value": 15, "delay": 2},
])