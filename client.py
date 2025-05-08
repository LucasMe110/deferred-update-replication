# client.py  
import socket  
import json  
import time  
import random  

class Client:  
    def __init__(self, cid, server_ports, sequencer_port):  
        self.cid = cid  
        self.server_ports = server_ports  
        self.sequencer_port = sequencer_port  
        self.write_set = []  
        self.read_set = []  

    def execute_transaction(self, operations):  
        selected_server = random.choice(self.server_ports)  
        print(f"Cliente {self.cid}: Executando transação no servidor {selected_server}")  

        for op in operations:  
            if op["type"] == "read":  
                self.handle_read(op["item"], selected_server)  
            elif op["type"] == "write":  
                self.handle_write(op["item"], op["value"])  
            elif op["type"] == "delay":  
                time.sleep(op["delay"])  

        self.send_commit()  

    def handle_read(self, item, server_port):  
        try:  
            # Verifica se o item está no write_set local  
            for entry in self.write_set:  
                if entry["item"] == item:  
                    self.read_set.append({"item": item, "version": -1})  
                    print(f"Cliente {self.cid}: Leitura de {item} = {entry['value']} (local)")  
                    return  

            # Consulta o servidor  
            s = None  
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                s.settimeout(3.0)  
                s.connect(("localhost", server_port))  
                request = {"operation": "read", "item": item}  
                s.send(json.dumps(request).encode())  
                
                response_data = s.recv(1024).decode()  
                response = json.loads(response_data)  
                
                if "status" in response and response["status"] == "error":  
                    print(f"Cliente {self.cid}: Erro no servidor: {response['message']}")  
                    return  
                
                self.read_set.append({  
                    "item": item,  
                    "version": response["version"]  
                })  
                print(f"Cliente {self.cid}: Leitura de {item} = {response['value']} (versão {response['version']})")  

            except Exception as e:  
                # Filtra o erro WinError 10038  
                if not (isinstance(e, OSError) and e.winerror == 10038):  
                    print(f"Erro na leitura: {str(e)}")  
            finally:  
                if s:  
                    s.close()  

        except Exception as e:  
            if not (isinstance(e, OSError) and e.winerror == 10038):  
                print(f"Erro na leitura: {str(e)}")  

    def handle_write(self, item, value):  
        self.write_set.append({"item": item, "value": value})  
        print(f"Cliente {self.cid}: Escrita de {item} = {value} (pendente)")  

    def send_commit(self):  
        try:  
            commit_request = {  
                "type": "commit",  
                "cid": self.cid,  
                "tid": f"t{random.randint(1000, 9999)}",  
                "rs": self.read_set,  
                "ws": self.write_set  
            }  

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.settimeout(3.0)  
            try:  
                s.connect(("localhost", self.sequencer_port))  
                s.send(json.dumps(commit_request).encode())  
                print(f"Cliente {self.cid}: Commit enviado (TID: {commit_request['tid']}).")  
            except Exception as e:  
                if not (isinstance(e, OSError) and e.winerror == 10038):  
                    print(f"Erro ao enviar commit: {str(e)}")  
            finally:  
                s.close()  

        except Exception as e:  
            if not (isinstance(e, OSError) and e.winerror == 10038):  
                print(f"Erro ao enviar commit: {str(e)}")  

if __name__ == "__main__":  
    SERVER_PORTS = [5001, 5002]  
    SEQUENCER_PORT = 6001  

    # Exemplo de uso  
    client = Client(1, SERVER_PORTS, SEQUENCER_PORT)  
    client.execute_transaction([  
        {"type": "read", "item": "x"},  
        {"type": "write", "item": "x", "value": 15}  
    ])