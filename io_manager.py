class IOManager:
    '''
    Classe que define o gerente de E/S
    '''
    scanner = None
    printer = [None, None]
    modem = None
    sata = [None, None]

    def aloca(self, processo):
        '''
        Analisa se os recursos estao disponiveis e aloca se estiverem
        '''

        free = True
        if processo['requisicao_modem'] == 1 and self.modem is not None:
            free = False
        if processo['requisicao_scanner'] == 1 and self.scanner is not None:
            free = False
        if processo['numero_impressora'] > 0 and self.printer[processo['numero_impressora'] - 1] is not None:
            free = False
        if processo['numero_disco'] > 0 and self.sata[processo['numero_disco'] - 1] is not None:
            free = False

        if free:
            if processo['requisicao_modem'] == 1:
                self.modem = processo['PID']
            if processo['requisicao_scanner'] == 1:
                self.scanner = processo['PID']
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
        if self.modem == processo['PID']:
            self.modem = None
        if self.scanner == processo['PID']:
            self.scanner = None
        if  processo['PID'] in self.printer:
            self.printer[processo['numero_impressora'] - 1] = None
        if  processo['PID'] in self.sata:
            self.sata[processo['numero_disco'] - 1] = None
