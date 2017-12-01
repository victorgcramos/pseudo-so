TAMANHO_TR = 64
TAMANHO_USUARIO = 960
class MemoryManager:

    tempo_real = [None for i in range(TAMANHO_TR)]
    usuario = [None for i in range(TAMANHO_USUARIO)]

    def salva (self, processo):
        offset = None
        if (processo['prioridade'] == 0):
            disponiveis = 0
            for i in range(TAMANHO_TR):
                bloco = self.tempo_real[i]
                if(bloco == None):
                    disponiveis += 1
                    if(disponiveis == processo['blocos_memoria']):
                        offset = i - disponiveis + 1
                        for j in range(disponiveis):
                            self.tempo_real[offset + j] = processo['PID']
                        break
                else:
                    disponiveis = 0
        else:
            disponiveis = 0
            for i in range(TAMANHO_USUARIO):
                bloco = self.usuario[i]
                if(bloco == None):
                    disponiveis += 1
                    if(disponiveis == processo['blocos_memoria']):
                        offset = i - disponiveis + 1
                        for j in range(disponiveis):
                            self.usuario[offset + j] = processo['PID']
                        break
                else:
                    disponiveis = 0
        return offset

    def mata (self, processo):
        if(processo['prioridade'] == 0):
            for i in range(processo['offset'], processo['offset'] + processo['blocos_memoria']):
                self.tempo_real[i] = None
        else:
            for i in range(processo['offset'], processo['offset'] + processo['blocos_memoria']):
                self.usuario[i] = None
