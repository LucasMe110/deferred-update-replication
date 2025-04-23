# client_test.py  
import socket  
import json  

def test_write_and_commit():  
    # Enviar escrita  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client_socket.connect(("localhost", 5001))  
    write_request = {  
        "operation": "write",  
        "item": "x",  
        "value": 10  
    }  
    client_socket.send(json.dumps(write_request).encode())  
    response = json.loads(client_socket.recv(1024).decode())  
    print(f"Resposta da escrita: {response}")  
    client_socket.close()  

    # Enviar commit via sequenciador (porta 6001)  
    commit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    commit_socket.connect(("localhost", 6001))  
    commit_request = {  
        "type": "commit",  
        "cid": 1,  
        "tid": "t1",  
        "rs": [{"item": "x", "version": 0}],  
        "ws": [{"item": "x", "value": 10}],  
        "sequence": 0  # O sequenciador atualizará para 1  
    }  
    commit_socket.send(json.dumps(commit_request).encode())  
    commit_socket.close()  

test_write_and_commit()  