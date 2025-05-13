| Arquivo                     | Objetivo                                                                                                                                     |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `client_concorrente.py`     | Testar **concorrência simultânea**: dois clientes leem e escrevem `x` ao mesmo tempo.                                                        |
| `teste_conflito_versoes.py` | Testar **conflito de versão por atraso**: um cliente começa antes, mas demora para commitar, permitindo que outro cliente "passe na frente". |


                [Cliente]
                   │
                   ▼
             ┌───────────┐
             │  Server   │ <────────────┐
             └───────────┘              │
     lê ou escreve x/y                  │
           │                            │
           ▼                            │
  escreve → vai para Sequencer → envia para todas as réplicas
                                           │
                                           ▼
                               process_commit: verifica versão e grava
