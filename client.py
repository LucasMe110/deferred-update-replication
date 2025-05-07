# client.py  
import socket  
import json  
import time  
import random  

class Client:  
    def __init__(self, cid, server_ports, sequencer_port):  
        self.cid = cid  
        self.server_ports = server_ports  # Lista de portas dos servidores (ex: [5001, 5002])  
        self.sequencer_port = sequencer_port  
        self.write_set = []  
        self.read_set = []  

    def execute_transaction(self, operations):  
        # Escolher um servidor aleatório para leituras  
        selected_server = random.choice(self.server_ports)  
        print(f"Cliente {self.cid}: Executando transação no servidor {selected_server}")  

        for op in operations:  
            if op["type"] == "read":  
                self.handle_read(op["item"], selected_server)  
            elif op["type"] == "write":  
                self.handle_write(op["item"], op["value"])  

            time.sleep(op.get("delay", 0))  # Simular atrasos entre operações  

        # Enviar commit  
        self.send_commit()  

    def handle_read(self, item, server_port):  
        try:  
            # Verificar se o item está no write_set local  
            for entry in self.write_set:  
                if entry["item"] == item:  
                    self.read_set.append({"item": item, "version": -1})  # Versão local não é relevante  
                    print(f"Cliente {self.cid}: Leitura de {item} = {entry['value']} (local)")  
                    return  

            # Se não está no write_set, consultar o servidor  
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
                s.connect(("localhost", server_port))  
                request = {"operation": "read", "item": item}  
                s.send(json.dumps(request).encode())  
                response = json.loads(s.recv(1024).decode())  
                self.read_set.append({"item": item, "version": response["version"]})  
                print(f"Cliente {self.cid}: Leitura de {item} = {response['value']} (versão {response['version']})")  

        except Exception as e:  
            print(f"Erro na leitura: {e}")  

    def handle_write(self, item, value):  
        self.write_set.append({"item": item, "value": value})  
        print(f"Cliente {self.cid}: Escrita de {item} = {value} (pendente)")  

    def send_commit(self):  
        try:  
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
                s.connect(("localhost", self.sequencer_port))  
                commit_request = {  
                    "type": "commit",  
                    "cid": self.cid,  
                    "tid": f"t{random.randint(1000, 9999)}",  
                    "rs": self.read_set,  
                    "ws": self.write_set  
                }  
                s.send(json.dumps(commit_request).encode())  
                print(f"\nCliente {self.cid}: Commit enviado (TID: {commit_request['tid']}).")  

        except Exception as e:  
            print(f"Erro ao enviar commit: {e}")  

# Exemplo de uso  
if __name__ == "__main__":  
    # Configurações  
    SERVER_PORTS = [5001, 5002]  # Portas dos servidores replicados  
    SEQUENCER_PORT = 6001  

    # Cliente 1: Transação sem conflito  
    client1 = Client(1, SERVER_PORTS, SEQUENCER_PORT)  
    client1.execute_transaction([  
        {"type": "read", "item": "x", "delay": 1},  
        {"type": "write", "item": "x", "value": 15, "delay": 2},  
    ])  