# Testes de Transações Distribuídas

Este documento descreve quatro cenários de teste para um sistema de transações distribuídas. Cada cenário tem como objetivo validar um aspecto específico do sistema.

---
> ```bash
>cd C:\workspaceufsc\DISTRIBUIDO\FINAL
> ```
## Cenário 1: Transação Sem Conflito

**Objetivo:** Mostrar que transações isoladas são efetivadas com sucesso.

### Passos:

1. Inicie o sequenciador e os dois servidores replicados:

   ```bash
   cd src/sequencer
   python sequencer.py
   ```
   ```bash
   cd src/server
   python server_1.py
   ```
   ```bash
   cd src/server
   python server_2.py
   ```
2. Execute o cliente 1:

   ```bash
   cd src/client
   python client1.py
   ```

---

## Cenário 2: Conflito de Versões

**Objetivo:** Demonstrar o aborto de transações com `read set` obsoleto.

### Passos:

1. Mantenha os servidores e o sequenciador em execução.
2. Execute o script de teste de conflito de versões:

   ```bash
   cd src/client
   python teste_conflito_versoes.py
   ```

---

## Cenário 3: Concorrência Entre Clientes

**Objetivo:** Simular transações concorrentes com alto risco de conflito.

### Passos:

1. Execute o script de clientes concorrentes:

   ```bash
   cd src/client
   python client_concorrente.py
   ```

---

## Cenário 4: Tolerância a Falhas

**Objetivo:** Mostrar como o sistema lida com réplicas defeituosas.

### Passos:

1. Inicie um servidor com falha:

   ```bash
   cd src/server
   python server_falha.py
   ```

2. Execute o cliente que se conecta à réplica com falha (porta 5003):

   ```bash
   cd src/client
   python cliente_teste_falha.py
   ```

---

