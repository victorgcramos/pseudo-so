from threading import Thread
import operator

class Process:
    def __init__(self, process):
        self.tempo_init = process[0]
        self.prioridade = process[1]
        self.tempo_processador = process[2]
        self.blocos_memoria = process[3]
        self.numero_impressora = process[4]
        self.requisicao_scanner = process[5]
        self.requisicao_modem = process[6]
        self.numero_disco = process[7]
        self.offset = None
        self.PID = None

class ProcessManager:
    fila_tempo_real = []
    fila_usuario = []
    prioridade_1 = []
    prioridade_2 = []
    prioridade_3 = []
    fila_principal = []
    em_execucao = {}
    ultimoPID = 0

    def escalona_processo_geral(self):
        """
        Escalona os processos nas filas de usuario ou fila de tempo real
        """

        if(not(self.fila_principal)):
            return False

        processo_topo = self.fila_principal[0]
        processo_topo['PID'] = self.ultimoPID
        self.ultimoPID += 1

        # distribui os processos ao longo das filas de usuario e tempo real
        if ((processo_topo['prioridade'] == 0) and (len(self.fila_tempo_real) < 1000)):
            self.fila_principal.pop(0)
            self.fila_tempo_real.append(processo_topo)

        elif (len(self.fila_usuario) < 1000):
            # alocou para a fila de usuario
            self.fila_principal.pop(0)
            self.fila_usuario.append(processo_topo)
        else:
            # Caso ele nao tenha conseguido alocar o processo nas filas
            return False
        return True

    def escalona_processo_usuario(self):
        """
        Escalona os processos de usuario nas filas de prioridades
        """
        if(not(self.fila_usuario)):
            return False

        processo_topo = self.fila_usuario[0]

        # aloca para a fila de prioridades
        if (processo_topo['prioridade'] == 1 and len(self.prioridade_1) < 1000):
            self.fila_usuario.pop(0)
            self.prioridade_1.append(processo_topo)
        elif (processo_topo['prioridade'] == 2 and len(self.prioridade_2) < 1000):
            self.fila_usuario.pop(0)
            self.prioridade_2.append(processo_topo)
        elif (processo_topo['prioridade'] == 3 and len(self.prioridade_3) < 1000):
            self.fila_usuario.pop(0)
            self.prioridade_3.append(processo_topo)
        else:
            return False

        return True
