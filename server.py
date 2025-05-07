# server.py  
import socket  
import threading  
import json  
import random  

class Server:  
    def __init__(self, port, sequencer_port):  
        self.db = {  
            "x": {"value": 0, "version": 0},  
            "y": {"value": 0, "version": 0}  
        }  
        self.port = port  
        self.host = "localhost"  
        self.sequencer_port = sequencer_port  

        # Socket para clientes  
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.server_socket.bind((self.host, self.port))  
        self.server_socket.listen(5)  
        print(f"Servidor iniciado em {self.host}:{self.port}")  

        # Registrar-se no sequenciador  
        self.register_with_sequencer()  

        # Socket para receber commits ordenados  
        self.commit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.commit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        self.commit_socket.bind((self.host, self.port + 3000))  
        self.commit_socket.listen(5)  

        # Sincronizar com outras réplicas ao iniciar  
        self.sync_with_replicas()  

        # Thread para ouvir commits  
        self.commit_thread = threading.Thread(target=self.listen_for_commits)  
        self.commit_thread.start()  

    def register_with_sequencer(self):  
        try:  
            reg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            reg_socket.connect((self.host, self.sequencer_port + 1000))  
            reg_socket.send(json.dumps({"port": self.port + 3000}).encode())  
            reg_socket.close()  
        except Exception as e:  
            print(f"Erro ao registrar no sequenciador: {e}")  

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
            
            elif request["operation"] == "write":  
                client_socket.send(json.dumps({"status": "write_pending"}).encode())  
            
            # Resposta a pedidos de sincronização de outras réplicas  
            elif request["operation"] == "sync":  
                client_socket.send(json.dumps(self.db).encode())  
                
        except Exception as e:  
            print(f"Erro: {e}")  
        finally:  
            client_socket.close()  

    def sync_with_replicas(self):  
        """Sincroniza o banco de dados com outras réplicas ao iniciar."""  
        replicas = [5001, 5002]  
        for replica_port in replicas:  
            if replica_port == self.port:  
                continue  
            try:  
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
                    s.connect((self.host, replica_port))  
                    s.send(json.dumps({"operation": "sync"}).encode())  
                    remote_db = json.loads(s.recv(1024).decode())  
                    for item in remote_db:  
                        if remote_db[item]["version"] > self.db.get(item, {"version": -1})["version"]:  
                            self.db[item] = remote_db[item]  
                    print(f"[SINCRONIZAÇÃO] Estado sincronizado com réplica {replica_port}")  
            except Exception as e:  
                print(f"[SINCRONIZAÇÃO] Falha ao sincronizar com {replica_port}: {str(e)}")  

    def listen_for_commits(self):  
        print(f"Ouvindo commits em {self.host}:{self.port + 3000}")  
        while True:  
            conn, addr = self.commit_socket.accept()  
            data = conn.recv(1024).decode()  
            commit_request = json.loads(data)  
            self.process_commit(commit_request)  
            conn.close()  

    def process_commit(self, commit_request):  
        print(f"\n[Servidor {self.port}] Processando commit da transação {commit_request['tid']}:")  
        print(f"Read Set: {commit_request['rs']}")  
        print(f"Write Set: {commit_request['ws']}")  
        
        abort = False  
        for item in commit_request["rs"]:  
            db_item = self.db.get(item["item"], {"version": -1})  
            if db_item["version"] > item["version"]:  
                print(f"Conflito detectado! Versão local de {item['item']}: {db_item['version']} > versão da transação: {item['version']}")  
                abort = True  
                break  
        
        if not abort:  
            for item in commit_request["ws"]:  
                self.db[item["item"]] = {  
                    "value": item["value"],  
                    "version": commit_request["sequence"]  
                }  
            print(f"✅ COMMIT: Transação {commit_request['tid']} efetivada. Novo estado do banco: {self.db}")  
        else:  
            print(f"❌ ABORT: Transação {commit_request['tid']} abortada (conflito de versões).")  

    def start(self):  
        while True:  
            client_socket, addr = self.server_socket.accept()  
            print(f"Conexão recebida de {addr}")  
            client_thread = threading.Thread(  
                target=self.handle_client,  
                args=(client_socket,)  
            )  
            client_thread.start()  