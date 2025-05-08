import subprocess  
import time  

# Reinicia o servidor após 10 segundos  
subprocess.Popen(["python", "server_1.py"])  
time.sleep(10)  
subprocess.Popen.kill()  # Encerra o servidor  
time.sleep(5)  
subprocess.Popen(["python", "server_1.py"])  # Reinicia  