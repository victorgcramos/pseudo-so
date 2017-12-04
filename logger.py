class Logger:
    last_exec = None

    def dispatch(self, processo):
        if(self.last_exec != -1 and self.last_exec != None):
            print('\tP{} INTERRUPTED'.format(self.last_exec))
        self.last_exec = -1
        print('dispatcher =>')
        print('\tPID:\t\t {}'.format(processo['PID']))
        print('\toffset:\t\t {}'.format(processo['offset']))
        print('\tblocks:\t\t {}'.format(processo['blocos_memoria']))
        print('\tpriority:\t {}'.format(processo['prioridade']))
        print('\ttime:\t\t {}'.format(processo['tempo_processador']))
        print('\tprinters:\t {}'.format(bool(processo['numero_impressora'])))
        print('\tscanner:\t {}'.format(bool(processo['requisicao_scanner'])))
        print('\tmodem:\t\t {}'.format(bool(processo['requisicao_modem'])))
        print('\tdrives:\t\t {}'.format(bool(processo['numero_disco'])))

    def executa(self, processo):
        if(self.last_exec != processo['PID']):
            if(self.last_exec is not -1):
                print('\tP{} INTERRUPTED'.format(self.last_exec))
            print('processo {} =>'.format(processo['PID']))
            if(processo['execucoes'] == 1):
                # import ipdb; ipdb.set_trace()
                print('\tP{} STARTED'.format(processo['PID']))
            else:
                print('\tP{} RESUMED'.format(processo['PID']))
        print('\tP{} instruction {}'.format(processo['PID'], processo['execucoes']))
        self.last_exec = processo['PID']
        if(processo['tempo_processador'] == 0):
            print('\tP{} return SIGINT'.format(processo['PID']))
            self.last_exec = -1

    def disco(self, fs):
        print('Sistema de Arquivos =>')
        i = 1
        for l in fs.log:
            print('\tOperacao {} => {}'.format(i, l['status']))
            print('\t\t{}'.format(l['mensagem']))
            i += 1
        for op in fs.operacoes:
            print('\tOperacao {} => Falha'.format(i))
            print('\t\tO processo {} nao existe'.format(op['PID']))
            i += 1
        print('\tMapa de Ocupacao de Disco:')
        print('\t\t{}'.format(fs.disco))
