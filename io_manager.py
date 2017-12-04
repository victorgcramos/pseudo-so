class IOManager:
    '''
    Classe que define o gerente de E/S
    '''
    scanner = [None]
    printer = [None, None]
    modem = [None]
    sata = [None, None]

    def aloca(self, processo):
        '''
        Analisa se os recursos estao disponiveis e aloca se estiverem
        '''

        free = True
        if processo['requisicao_modem'] > 0 and self.modem[0] is not None:
            free = False
        if processo['requisicao_scanner'] > 0 and self.scanner[0] is not None:
            free = False
        if processo['numero_impressora'] > 0 and self.printer[processo['numero_impressora'] - 1] is not None:
            free = False
        if processo['numero_disco'] > 0 and self.sata[processo['numero_disco'] - 1] is not None:
            free = False
        if free:
            if processo['requisicao_modem'] > 0:
                self.modem[0] = processo['PID']
            if processo['requisicao_scanner'] > 0:
                self.scanner[0] = processo['PID']
            if processo['numero_impressora'] > 0:
                self.printer[processo['numero_impressora'] - 1] = processo['PID']
            if processo['numero_disco'] > 0:
                self.printer[processo['numero_disco'] - 1] = processo['PID']
            return True
        else:
            return False
    def libera(self, processo):
        '''
        Libera todos os recursos utilizados pelo processo
        '''
        if self.modem[0] == processo['PID']:
            self.modem[0] = None
        if self.scanner[0] == processo['PID']:
            self.scanner[0] = None
        if  processo['PID'] in self.printer:
            self.printer[processo['numero_impressora'] - 1] = None
        if  processo['PID'] in self.sata:
            self.sata[processo['numero_disco'] - 1] = None
