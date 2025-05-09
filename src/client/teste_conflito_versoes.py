# teste_conflito_versoes.py
from client import Client
import time
import threading

def cliente_1():
    """Lê x (versão 0), escreve x=20, mas demora para commitar."""
    client = Client(1, [5001, 5002], 6001)
    print("\n--- Cliente 1 Iniciado ---")
    # Fase de Execução
    client.execute_transaction([
        {"type": "read", "item": "x"},                    # Lê x (versão 0)
        {"type": "write", "item": "x", "value": 20},       # Escreve x=20 localmente
        {"type": "delay", "delay": 5}                      # Delay para forçar conflito
    ])
    # O commit será enviado automaticamente após o delay

def cliente_2():
    """Escreve x=30 e commita imediatamente, antes do Cliente 1."""
    client = Client(2, [5001, 5002], 6001)
    print("\n--- Cliente 2 Iniciado ---")
    client.execute_transaction([
        {"type": "write", "item": "x", "value": 30}        # Escreve x=30 e commita
    ])

if __name__ == "__main__":
    # Iniciar Cliente 1 (irá esperar 5 segundos após a escrita)
    cliente_1_thread = threading.Thread(target=cliente_1)
    cliente_1_thread.start()
    
    # Aguardar 2 segundos para iniciar Cliente 2 durante o delay do Cliente 1
    time.sleep(2)
    
    # Iniciar Cliente 2 (irá commitar antes do Cliente 1)
    cliente_2_thread = threading.Thread(target=cliente_2)
    cliente_2_thread.start()