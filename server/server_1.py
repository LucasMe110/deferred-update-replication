# server_1.py  
from server import Server  

if __name__ == "__main__":  
    server = Server(5001, 6001)  # Porta 5001 e sequenciador na 6001  
    server.start()  