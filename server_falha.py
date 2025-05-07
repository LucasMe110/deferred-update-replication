#server_falha.py
from server import Server
import json

class ServerFalha(Server):
    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            request = json.loads(data)
            
            # Falha determinística em operações de leitura/escrita
            print(f"[FALHA] Servidor {self.port} rejeitou operação!")
            client_socket.send(json.dumps({
                "status": "error",
                "message": "Servidor em modo de falha."
            }).encode())
            
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            client_socket.close()

    def process_commit(self, commit_request):
        # Bloquear commits sempre!
        print(f"[FALHA] Servidor {self.port} ignorou commit {commit_request['tid']}!")
        # Não atualizar o banco de dados
        print(f"ABORT: Transação {commit_request['tid']} abortada (servidor em falha).")

if __name__ == "__main__":
    server = ServerFalha(5003, 6001)  # Porta 5003
    server.start()