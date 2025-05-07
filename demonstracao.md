Cenário 1: Transação Sem Conflito
Objetivo: Mostrar que transações isoladas são efetivadas com sucesso.
Passos:

Inicie o sequenciador e dois servidores replicados:

python sequencer.py  

python server_1.py  

python server_2.py 


Execute o cliente 1 (client1.py):

python client1.py  


Cenário 2: Conflito de Versões
Objetivo: Demonstrar o aborto de transações com read set obsoleto.
Passos:

Mantenha os servidores e sequenciador em execução.
Execute teste_conflito_versoes.py

teste_conflito_versoes.py


Cenário 3: Concorrência Entre Clientes
Objetivo: Simular transações concorrentes com alto risco de conflito.
Passos:

Execute client_concorrente.py:

Cenário 4: Tolerância a Falhas
Objetivo: Mostrar como o sistema lida com réplicas defeituosas.
Passos:

Inicie um servidor com falha (server_falha.py):

python server_falha.py  

Execute cliente_teste_falha.py (conecta-se ao servidor 5003):

python cliente_teste_falha.py  
