# server_2.py  
from server import Server  

if __name__ == "__main__":  
    server = Server(5002, 6001)  # Porta 5002 e sequenciador na 6001  
    server.start()  