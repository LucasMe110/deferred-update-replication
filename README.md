O problema proposto neste trabalho é desenvolver uma solução para permitir que múltiplos clientes possam acessar e modificar dados compartilhados de forma simultânea em um sistema distribuído, garantindo que essas modificações sejam consistentes entre várias réplicas de servidores, mesmo sem uma coordenação constante entre eles. Para isso, será implementado o protocolo de Replicação com Atualização Adiada (DUR), que permite que as transações sejam executadas localmente pelos clientes sem bloquear recursos ou depender de comunicação imediata com os servidores, armazenando temporariamente as operações realizadas até que seja necessário decidir se a transação deve ser confirmada ou abortada. Essa decisão é tomada de forma coordenada entre todos os servidores por meio de uma difusão atômica das informações de leitura e escrita, garantindo que todos os servidores cheguem à mesma conclusão de forma ordenada. O desafio está em controlar corretamente essa concorrência, evitando que uma transação confirme mudanças baseadas em dados que já foram alterados por outras, e ao mesmo tempo manter a eficiência e disponibilidade do sistema mesmo com múltiplos clientes concorrendo pelo acesso aos dados.

cd C:\workspaceufsc\DISTRIBUIDO\FINAL


liga a apicação
python sequencer.py  

python server_1.py

python server_2.py  


teste 1


teste 2
python client1.py  
roda rapido para dar conflito
python client2.py  


teste 3
O que o client_concorrente.py testa?
Conflito de Escrita-Escrita:

Dois clientes (A e B) tentam atualizar o mesmo item (x) com valores diferentes (100 e 200) ao mesmo tempo.

Objetivo: Verificar se o sistema detecta o conflito e garante que apenas uma transação seja efetivada.

Consistência após Concorrência:

Garantir que, mesmo com transações concorrentes, o banco de dados final mantenha consistência entre as réplicas.

Ordem Total de Commits:

Validar que o sequenciador ordena os commits corretamente e que todas as réplicas processam as transações na mesma ordem.


python client_concorrente.py  