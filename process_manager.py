from threading import Thread
import operator

class Process:
    def __init__(self):
        self.tempo_init = 0
        self.prioridade = 0
        self.tempo_processador = 0
        self.blocos_memoria = 0
        self.numero_impressora = 0
        self.requisicao_scanner = 0
        self.requisicao_modem = 0
        self.numero_disco = 0

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
        if (processo_topo['prioridade'] == 0 && len(self.fila_tempo_real) < 1000):
            self.fila_principal.pop()
            self.fila_tempo_real.insert(0, processo_topo)

        elif (len(self.fila_usuario) < 1000):
            # alocou para a fila de usuario
            self.fila_principal.pop()
            self.fila_usuario.insert(0, processo_topo)
        else:
            # Caso ele não tenha conseguido alocar o processo nas filas
            return False
        return True

    def escalona_processo_usuario(self):
        """
        Escalona os processos de usuario nas filas de prioridades
        """
        processo_topo = fila_usuario[len(self.fila_usuario) - 1]
        # aloca para a fila de prioridades
        if len(prioridade_1) < 1000:
            self.prioridade_1.insert(0, processo_topo)
        else:
            return False
        return True

#  tem que pegar o processo de menor prioridade
    def muda_prioridade(self):
        # ordena o array por prioridade
        self.prioridade_1.sort(key=operator.itemgetter('prioridade'))
        p_troca = {}
        # pega o elemento da fila_usuario
        processo = self.fila_usuario.pop()
        # se esse elemento possuir uma prioridade maior que o de menor prioridade
        if processo['prioridade'] > self.prioridade_1[len(self.prioridade_1)]['prioridade']:
            p_troca = self.prioridade_1.pop()
            self.prioridade_1.insert(0, processo)
            if p_troca['prioridade'] > 
