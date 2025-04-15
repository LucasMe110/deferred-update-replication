# server.py
import socket
import threading
import json

class Server:
    def __init__(self, port):
        self.db = {
            "x": {"value": 0, "version": 0},
            "y": {"value": 0, "version": 0}
        }
        self.port = port
        self.host = "localhost"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            request = json.loads(data)
            
            if request["operation"] == "read":
                item = request["item"]
                response = {
                    "value": self.db[item]["value"],
                    "version": self.db[item]["version"]
                }
                client_socket.send(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            client_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexão recebida de {addr}")
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket,)
            )
            client_thread.start()

if __name__ == "__main__":
    # Iniciar servidores em portas diferentes (ex: 5001, 5002, 5003)
    server = Server(5001)
    server.start()