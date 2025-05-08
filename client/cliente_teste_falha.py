# cliente_teste_falha.py  
from client import Client  

client = Client(99, [5003], 6001)  # Forçar conexão ao servidor com falha  
client.execute_transaction([  
    {"type": "read", "item": "x"},  
    {"type": "write", "item": "x", "value": 100},  
])  