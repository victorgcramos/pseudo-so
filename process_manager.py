from threading import Thread

class Process:
    tempo_init = 0
    prioridade = 0
    tempo_processador = 0
    blocos_memoria = 0
    numero_impressora = 0
    requisicao_scanner = 0
    requisicao_modem = 0
    numero_disco = 0

class ProcessManager:
    fila_tempo_real = []
    fila_usuario = []
    prioridade_1 = []
    prioridade_2 = []
    prioridade_3 = []
    fila_principal = []

    def novo_processo(self, processo):
        """
        insere o processo na fila principal
        """
        self.fila_principal.insert(0, processo)

    def escalona_processo_geral(self):
        """
        Escalona os processos nas filas de usuario ou fila de tempo real
        """
        processo_topo = self.fila_principal[len(self.fila_principal) - 1]

        # distribui os processos ao longo das filas de usuario e tempo real
        if (processo_topo.prioridade == 0 && len(self.fila_tempo_real) < 1000):
            self.fila_principal.pop()
            self.fila_tempo_real.insert(0, processo_topo)

        elif (len(self.fila_usuario) < 1000):
            # alocou para a fila de usuario
            self.fila_principal.pop()
            self.fila_usuario.insert(0, processo_topo)

    def escalona_processo_usuario(self):
        """
        Escalona os processos de usuario nas filas de prioridades
        """
        processo_topo = fila_usuario[len(self.fila_usuario) - 1]
        # aloca para a fila de prioridades
        if (proceso_topo.prioridade == 1):
            self.prioridade_1.insert(0, processo_topo)
        elif (proceso_topo.prioridade == 2):
            self.prioridade_2.insert(0, processo_topo)
        elif (proceso_topo.prioridade == 3):
            self.prioridade_3.insert(0, processo_topo)
