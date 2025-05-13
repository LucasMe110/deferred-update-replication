# Distributed Deferred Update Replication (DUR)

Este projeto implementa o protocolo **Deferred Update Replication (DUR)** para sistemas distribuídos, conforme apresentado na disciplina de Mestrado em Computação Distribuída. O uso de DUR busca garantir consistência e replicação de dados em múltiplas réplicas, detectando conflitos de versão antes de aplicar commits.

---

## Motivação e Problema

Em ambientes distribuídos, garantir a **ordenação total** de commits e a **consistência** entre réplicas é um desafio clássico. Falhas de comunicação, concorrência de transações e quedas de servidores podem levar a divergências de estado. O protocolo DUR aborda esses problemas por meio de:

* **Difusão Atômica**: uso de um *sequencer* para atribuir números de sequência a commits, assegurando ordem total.
* **Fase de Execução**: clientes acumulam localmente operações de leitura e escrita, sem tocar nas réplicas até o commit.
* **Fase de Terminação**: envio de certificado (`read_set` + `write_set`) ao sequencer e redistribuição ordenada às réplicas.
* **Teste de Certificação**: réplicas verificam conflitos de versão e abortam transações que violam ordem causal.

Este trabalho surgiu como parte do curso de Mestrado em **Computação Distribuída** e explora como replicação primária-múltipla com ordenação centralizada pode simplificar garantias de consistência.

---

## Arquitetura do Projeto

```
meu_projeto/
├── client/                      # Entrypoints dos clientes
│   ├── client1.py               # Cliente 1: exemplo de transação
│   ├── client2.py               # Cliente 2: exemplo concorrente
│   ├── cliente_teste_falha.py   # Simulação de servidor em falha
│   └── teste_conflito_versoes.py# Teste de abortos por conflito
│
├── server/                      # Entrypoints dos servidores
│   ├── server_1.py              # Inicia réplica na porta 5001
│   ├── server_2.py              # Inicia réplica na porta 5002
│   └── server_falha.py          # Servidor que rejeita operações
│
├── sequencer/                   # Sequenciador de commits
│   └── sequencer.py             # Orquestra ordenação total
│
├── docs/                        # Documentação de suporte
│   ├── INE5410130_trabalho.pdf  # Enunciado da disciplina
│   ├── Relatorio_DUR_LucasMello.pdf # Relatório de implementação
│   └── testes_transacoes_distribuidas.md # Plano de testes
│
└── README.md                    # (você está aqui)
```

### Componentes principais

* **Client** (`client/`): classe `Client` que realiza execução e commit de transações.
* **Sequencer** (`sequencer/sequencer.py`): centraliza a ordenação de commits.
* **Server** (`server/`): objetos `Server` que aplicam teste de certificação e replicam estado.

---

## Como usar

1. **Pré-requisitos**

   * Python 3.7+ instalado
   * (Opcional) `pip install -r requirements.txt` caso use bibliotecas adicionais

2. **Inicializar o Sequencer**

   ```bash
   cd src/sequencer
   python sequencer.py
   ```

3. **Subir Réplicas** (em terminais separados)

   ```bash
   cd src/server
   python server_1.py
   python server_2.py
   ```

4. **Executar Clientes**

   ```bash
   cd src/client
   python client1.py
   python client2.py
   # Outros scripts de teste disponíveis
   ```

---

## Testes de Transações Distribuídas

Este documento descreve quatro cenários de teste para um sistema de transações distribuídas. Cada cenário tem como objetivo validar um aspecto específico do sistema.

> Caminho base sugerido:
>
> ```bash
> cd C:\workspaceufsc\DISTRIBUIDO\FINAL
> ```

### Cenário 1: Transação Sem Conflito

**Objetivo:** Mostrar que transações isoladas são efetivadas com sucesso.

```bash
python sequencer.py
```
```bash
python server_1.py
```
```bash
python server_2.py
```
```bash
python client1.py
```

### Cenário 2: Conflito de Versões

**Objetivo:** Demonstrar o aborto de transações com `read set` obsoleto.

```bash
python teste_conflito_versoes.py
```

### Cenário 3: Concorrência Entre Clientes

**Objetivo:** Simular transações concorrentes com alto risco de conflito.

```bash
python client_concorrente.py
```

### Cenário 4: Tolerância a Falhas

**Objetivo:** Mostrar como o sistema lida com réplicas defeituosas.

```bash
python server_falha.py
```

```bash
python cliente_teste_falha.py
```

---

## Documentação

Veja a pasta `docs/` para:

* Enunciado e requisitos (INE5410130\_trabalho.pdf)
* Relatório detalhado de implementação (Relatorio\_DUR\_LucasMello.pdf)
* Plano de testes (testes\_transacoes\_distribuidas.md)

---

## Autor

Este projeto foi desenvolvido por **Lucas Mello Muller de Oliveira** como parte da disciplina de Mestrado em Computação Distribuída.






