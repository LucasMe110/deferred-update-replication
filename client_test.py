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