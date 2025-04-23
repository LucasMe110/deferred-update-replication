# client_test.py
import socket
import json

def send_read_request(port, item):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", port))
    request = {
        "operation": "read",
        "item": item
    }
    client_socket.send(json.dumps(request).encode())
    response = json.loads(client_socket.recv(1024).decode())
    print(f"Resposta do servidor na porta {port}: {response}")
    client_socket.close()

# Testar leitura de 'x' no servidor da porta 5001
send_read_request(5001, "x")

# client.py (atualizado)
class Client:
    def commit_transaction(self, tid, rs, ws):
        commit_request = {
            "type": "commit",
            "cid": self.cid,
            "tid": tid,
            "rs": rs,
            "ws": ws
        }
        commit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        commit_socket.connect(("localhost", 6001))  # Conectar ao sequenciador
        commit_socket.send(json.dumps(commit_request).encode())
        commit_socket.close()