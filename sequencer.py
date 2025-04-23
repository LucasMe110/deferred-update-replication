# sequencer.py
import socket
import threading
import json

class Sequencer:
    def __init__(self, port):
        self.port = port
        self.host = "localhost"
        self.sequence_number = 0
        self.replica_servers = []  # Lista de servidores replicados registrados
        self.lock = threading.Lock()

        # Socket para receber commits de clientes
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind((self.host, self.port))
        self.client_socket.listen(5)
        print(f"Sequenciador iniciado em {self.host}:{self.port}")

        # Socket para registro de servidores replicados
        self.replica_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.replica_socket.bind((self.host, port + 1000))  # Ex: 7001 se porta for 6001
        self.replica_socket.listen(5)
        print(f"Aguardando registro de servidores em {self.host}:{port + 1000}")

        # Thread para aceitar servidores replicados
        replica_thread = threading.Thread(target=self.handle_replica_registration)
        replica_thread.start()

    def handle_replica_registration(self):
        while True:
            replica_conn, addr = self.replica_socket.accept()
            data = replica_conn.recv(1024).decode()
            replica_info = json.loads(data)
            print(f"Servidor replicado registrado: {addr} (porta de commits: {replica_info['port']})")
            self.replica_servers.append({
                "conn": replica_conn,
                "commit_port": replica_info["port"]
            })

    def handle_client_commit(self, client_conn):
        try:
            data = client_conn.recv(1024).decode()
            commit_request = json.loads(data)
            
            with self.lock:
                self.sequence_number += 1
                commit_request["sequence"] = self.sequence_number

                for replica in self.replica_servers:
                    try:
                        commit_port = replica["commit_port"]
                        replica_commit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        replica_commit_socket.connect(("localhost", commit_port))  # Usa a porta armazenada!
                        replica_commit_socket.send(json.dumps(commit_request).encode())
                        replica_commit_socket.close()
                    except Exception as e:
                        print(f"Erro ao enviar commit para réplica: {e}")
                        self.replica_servers.remove(replica)

            print(f"Commit sequenciado: {commit_request}")
                
        except Exception as e:
            print(f"Erro no sequenciador: {e}")
        finally:
            client_conn.close()

    def start(self):
        while True:
            client_conn, addr = self.client_socket.accept()
            print(f"Commit recebido de {addr}")
            commit_thread = threading.Thread(
                target=self.handle_client_commit,
                args=(client_conn,)
            )
            commit_thread.start()

if __name__ == "__main__":
    sequencer = Sequencer(6001)  # Porta para commits
    sequencer.start()