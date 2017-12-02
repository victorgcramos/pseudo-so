TAMANHO_TR = 64
TAMANHO_USUARIO = 960
class MemoryManager:

    memoria = [None for i in range(TAMANHO_TR + TAMANHO_USUARIO)]

    def salva (self, processo):
        offset = None
        disponiveis = 0
        start = 0
        end = TAMANHO_TR+TAMANHO_USUARIO
        if processo['prioridade'] > 0:
            start = TAMANHO_TR
        else:
            end = TAMANHO_TR
        for i in range(start, end):
            bloco = self.memoria[i]
            if(bloco == None):
                disponiveis += 1
                if(disponiveis == processo['blocos_memoria']):
                    offset = i - disponiveis + 1
                    self.memoria[offset:offset+disponiveis] = processo['blocos_memoria'] * [processo['PID']]
                    break
            else:
                disponiveis = 0
        return offset

    def mata (self, processo):
        self.memoria[processo['offset']: processo['offset'] + processo['blocos_memoria']] =  processo['blocos_memoria']*[None]
