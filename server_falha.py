# server_falha.py
from server import Server
import json

class ServerFalha(Server):
    def sync_with_replicas(self):
        """Não sincroniza com outras réplicas."""
        replicas = []  # Lista vazia
        print("[SINCRONIZAÇÃO] Servidor em modo de falha ignora sincronização.")

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            request = json.loads(data)
            
            print(f"[FALHA] Servidor {self.port} rejeitou operação!")
            
            # Resposta padronizada para todas as operações
            response = {
                "status": "error",
                "message": "Servidor em modo de falha.",
                "value": None,
                "version": -1
            }
            client_socket.send(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            client_socket.close()

    def process_commit(self, commit_request):
        print(f"[FALHA] Servidor {self.port} ignorou commit {commit_request['tid']}!")
        # Força abort e notifica o cliente
        print(f"ABORT: Transação {commit_request['tid']} abortada (servidor em falha).")
        return "abort"

if __name__ == "__main__":
    server = ServerFalha(5003, 6001)
    server.start()