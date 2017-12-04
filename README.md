# Trabalho de Sistemas Operacionais

## Gerenciador de processos

Nossa estrutura de processos consiste em um dicionário do tipo:
```json
  "processo": {
    "tempo_init": 0,
    "prioridade": 0,
    "tempo_processador": 0,
    "blocos_memoria": 0,
    "numero_impressora": 0,
    "requisicao_scanner": 0,
    "requisicao_modem": 0,
    "numero_disco": 0,
    "PID": 0,
    "offset": 0,
  }
```
As filas de processos estão seguindo o esquema proposto na especificação, sendo
assim, os processos são escalonados em 1 fila: "fila_principal", e depois redi-
recionados para outras demais filas: "fila_tempo_real", e "fila_usuario".

Os processos da fila_tempo_real são os de prioridade = 0, e nas fila de usuário,
os demais processos.

### fila de usuário
A fila_usuário é composta por processos de usuário. Eles são escalonados nas demais
filas: "prioridade_1", "prioridade_2", e "prioridade_3". E são realocados nessas filas
de acordo com sua prioridade.
