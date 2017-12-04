class File:
    '''
    Arquivo no disco
    '''
    def __init__(self, arquivo, criador=None):
        self.nome = arquivo[0]
        self.bloco_inicio = int(arquivo[1])
        self.tamanho = int(arquivo[2])
        self.criador = criador

class FileOperation:
    '''
    Operacoes em arquivos
    '''
    def __init__(self, operacao):
        self.PID = int(operacao[0])
        self.opcode = int(operacao[1])
        self.arquivo = operacao[2]
        if(self.opcode == 0):
            self.tamanho = int(operacao[3])
        else:
            self.tamanho = None

class FileManager:
    '''
    Gerencia arquivos e operacoes dos processos sobre eles
    '''
    qtd_blocos = 0
    qtd_segmentos = 0
    arquivos = []
    operacoes = []
    #Lista de blocos do disco
    disco = []
    #Saidas do gerenciador de arquivos
    log = []

    def inicia_disco(self):
        '''
        Inicializa o disco com os arquivos descritos no arquivo de entrada
        '''
        self.disco = [0 for i in range(self.qtd_blocos)]
        for arq in self.arquivos:
            self.disco[arq['bloco_inicio']:arq['bloco_inicio'] + arq['tamanho']] = arq['tamanho']*[arq['nome']]

    def cria_arquivo(self, nome, tamanho, criador):
        '''
        Cria novo arquivo no disco
        '''
        offset = None
        disponiveis = 0

        if (next((arq for arq in self.arquivos if arq['nome'] == nome), None) is not None):
            self.log.append({
                "status": 'Falha',
                "mensagem": 'O processo {} nao criou o arquivo {} (Arquivo ja existe no disco)'.format(
                criador, nome
                )
            })
            return

        #localiza espaco disponivel com First Fit e armazena
        for i in range(self.qtd_blocos):
            bloco = self.disco[i]
            if(bloco == 0):
                disponiveis += 1
                if(disponiveis == tamanho):
                    offset = i - disponiveis + 1
                    self.disco[offset:offset+disponiveis] = tamanho * [nome]
                    arquivo = File([nome, offset, tamanho], criador=criador)
                    self.arquivos.append(arquivo.__dict__)
                    self.log.append({
                        "status": 'Sucesso',
                        "mensagem": 'O processo {} criou o arquivo {} (blocos {})'.format(
                        criador, nome, range(offset,offset+disponiveis))
                    })
                    return
            else:
                disponiveis = 0
        self.log.append({
            "status": 'Falha',
            "mensagem": 'O processo {} nao criou o arquivo {} (Sem espaco livre)'.format(
            criador, nome
            )
        })

    def deleta_arquivo(self, arquivo):
        '''
        Remove arquivo do disco
        '''
        self.disco[arquivo['bloco_inicio']:arquivo['bloco_inicio'] + arquivo['tamanho']] =  arquivo['tamanho']*[0]

    def opera_processo(self, processo):
        '''
        Executa todas as operacoes de um processo
        '''
        #Localiza as operacoes pertencentes ao processo
        ops = [op for op in self.operacoes if op['PID'] == processo['PID']]
        for op in ops:
            #CODIGO PARA CRIACAO
            if op['opcode'] == 0:
                self.cria_arquivo(op['arquivo'], op['tamanho'], processo['PID'])
            #CODIGO PARA DELECAO
            else:
                # Seleciona o arquivo pra ser deletado
                arquivo = next((arq for arq in self.arquivos if arq['nome'] == op['arquivo']), None)

                if arquivo is not None:
                    #Avalia permissoes
                    if (processo['prioridade'] == 0) or (arquivo['criador'] == None or processo['PID'] == arquivo['criador']):
                        self.deleta_arquivo(arquivo)
                        self.log.append({
                            "status": 'Sucesso',
                            "mensagem":'O processo {} deletou o arquivo {}'.format(
                            processo['PID'], arquivo['nome'])
                        })
                    else:
                        self.log.append({
                            "status": 'Falha',
                            "mensagem":'O processo {} nao pode deletar o arquivo {} (Erro de permissao)'.format(
                            processo['PID'], arquivo['nome'])
                        })
                else:
                    self.log.append({
                        "status": 'Falha',
                        "mensagem":'O processo {} nao pode deletar o arquivo {} (Arquivo Inexistente)'.format(
                        processo['PID'], op['arquivo'])
                    })
            self.operacoes.remove(op)
