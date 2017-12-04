#Constantes de tamanho da memoria
TAMANHO_TR = 64
TAMANHO_USUARIO = 960

class MemoryManager:
    ''' Classe do gerenciador de memoria

        CAMPOS: memoria - lista de blocos da memoria
    '''

    memoria = [None for i in range(TAMANHO_TR + TAMANHO_USUARIO)]

    def salva (self, processo):
        ''' Armazena processo na memoria, retorna None se nao foi posssvel armazenar, o
        offset caso contrario
        '''
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
        ''' Remove o processo da memoria
        '''
        self.memoria[processo['offset']: processo['offset'] + processo['blocos_memoria']] =  processo['blocos_memoria']*[None]
