import memory_manager as mm
import io_manager as iom
import file_manager as fm
import process_manager as pm
import logger as log
import operator
import sys


def main ():
    ''' Main que simula o dispatcher, administra todos os modulos e le os Arquivos
    de entrada '''

    #Inicializa modulos
    manager = pm.ProcessManager()
    memory = mm.MemoryManager()
    io = iom.IOManager()
    filesystem = fm.FileManager()
    logger = log.Logger()

    # Se tiver dois argumentos de linha, utiliza-os, senao usa os padroes
    if len(sys.argv) > 2:
        procFile = sys.argv[1]
        arqFile = sys.argv[2]
    else:
        procFile = 'processes.txt'
        arqFile = 'files.txt'

    #Abre e le o arquivo de processos
    with open(procFile, 'r') as f:
        procs = [[int(x) for x in line.split(',')] for line in f]
        processes = [pm.Process(x).__dict__ for x in procs]

    #Abre e le o arquivo do sistema de arquivos
    with open(arqFile, 'r') as f:
        temp = f.read().splitlines()
        filesystem.qtd_blocos = int(temp[0])
        filesystem.qtd_segmentos = int(temp[1])
        filesystem.arquivos = [fm.File(temp[i].replace(' ', '').split(',')).__dict__
                                for i in range(2, filesystem.qtd_segmentos+2)]
        filesystem.operacoes = [fm.FileOperation(temp[i].replace(' ', '').split(',')).__dict__
                                for i in range(filesystem.qtd_segmentos+3, len(temp))]

    filesystem.inicia_disco()
    #Ordena os processos por ordem de chegada
    manager.fila_principal = list(sorted(processes, key=operator.itemgetter('tempo_init')))
    # Como o quantum e um, o tratamento e apenas um iterador t
    t = 0
    while(True):
        #Se tiver processo ainda nao processado
        while(manager.fila_principal):
            #Escalona processos do tempo de chegada = t
            if(manager.fila_principal[0]['tempo_init'] == t):
                manager.escalona_processo_geral()
            else:
                break
        #Escalona processos da fila de usuario para as filas de prioridade
        while(manager.escalona_processo_usuario()):
            pass
        #SE NAO TEM NADA EXECUTANDO(SE TIVER VAI SER TEMPO REAL)
        if(not(manager.em_execucao)):
            #Executa tempo real se tiver
            if(manager.fila_tempo_real):
                #Tenta salvar na memoria, se tiver espaco
                manager.fila_tempo_real[0]['PID'] = manager.gera_pid()
                offset = memory.salva(manager.fila_tempo_real[0])
                #Coloca em execucao
                if(offset is not None):
                    manager.em_execucao = manager.fila_tempo_real.pop(0)
                    manager.em_execucao['offset'] = offset
                    logger.dispatch(manager.em_execucao)
                #Nao atribui PID se n conseguir salvar na memoria
                else:
                    manager.fila_tempo_real[0]['PID'] = None
                    manager.ultimoPID -= 1

            #Se nao tiver tempo real, vai ser despachado processos de usuario
            elif(manager.prioridade_1 or manager.prioridade_2 or manager.prioridade_3):
                # Procura algum processo de prioridade 1 que possa ser executado
                for novo_processo in manager.prioridade_1:
                    #Se processo ainda nao esta na memoria(nunca foi executado)
                    if novo_processo['offset'] is None:
                        #Ve se pode ser alocado em IO
                        novo_processo['PID'] = manager.gera_pid()
                        if(io.aloca(novo_processo)):
                            offset = memory.salva(novo_processo)
                            novo_processo['offset'] = offset
                            logger.dispatch(novo_processo)
                    offset = novo_processo['offset']
                    #Se o processo puder ser executado, carrega para a CPU
                    if(offset is not None):
                        manager.em_execucao = manager.prioridade_1.pop(manager.prioridade_1.index(novo_processo))
                        break
                    else:
                        novo_processo['PID'] = None
                        manager.ultimoPID -= 1

                # Se nao pode atribuir processos de prioridade 1(falta de processos ou recursos(memoria e io))
                if(manager.em_execucao == {}):
                    for novo_processo in manager.prioridade_2:
                        #Se processo ainda nao esta na memoria
                        if novo_processo['offset'] is None:
                            #Ve se pode ser alocado em IO
                            novo_processo['PID'] = manager.gera_pid()
                            if(io.aloca(novo_processo)):
                                offset = memory.salva(novo_processo)
                                novo_processo['offset'] = offset
                                logger.dispatch(novo_processo)
                        offset = novo_processo['offset']
                        #Se o processo puder ser executado, carrega para a CPU
                        if(offset is not None):
                            manager.em_execucao = manager.prioridade_2.pop(manager.prioridade_2.index(novo_processo))
                            break
                        else:
                            novo_processo['PID'] = None
                            manager.ultimoPID -= 1

                    # Se nao pode atribuir processos de prioridade 1 ou 2(falta de processos ou recursos(memoria e io))
                    if(manager.em_execucao == {}):
                        for novo_processo in manager.prioridade_3:
                            #Se processo ainda nao esta na memoria
                            if novo_processo['offset'] is None:
                                #Ve se pode ser alocado em IO
                                novo_processo['PID'] = manager.gera_pid()
                                if(io.aloca(novo_processo)):
                                    offset = memory.salva(novo_processo)
                                    novo_processo['offset'] = offset
                                    logger.dispatch(novo_processo)
                            offset = novo_processo['offset']
                            #Se o processo puder ser executado, carrega para a CPU
                            if(offset is not None):
                                manager.em_execucao = manager.prioridade_3.pop(manager.prioridade_3.index(novo_processo))
                                break
                            else:
                                novo_processo['PID'] = None
                                manager.ultimoPID -= 1
            elif(not (manager.fila_principal)):
                #Condicao de saida do programa => Nao tem nenhum processo em nenhuma fila
                #E todos os processos ja chegaram
                break
        # Executa Processo
        if(manager.em_execucao):
            #Decrementa tempo restante e aumenta o numero de instrucoes rodadas
            manager.em_execucao['tempo_processador'] -= 1
            manager.em_execucao['execucoes'] += 1
            #Mostra Saida
            logger.executa(manager.em_execucao)
            #APOS EXECUCAO
            #Remove o processo da memoria e libera recursos SE TIVER ACABADO O TEMPO
            if manager.em_execucao['tempo_processador'] == 0:
                filesystem.opera_processo(manager.em_execucao)
                io.libera(manager.em_execucao)
                memory.mata(manager.em_execucao)
                manager.em_execucao = {}
            #COmo o quantum eh um, processos de usuario sao retirados da CPU em toda iteracao
            elif manager.em_execucao['prioridade'] > 0:
                if manager.em_execucao['prioridade'] == 1:
                    manager.prioridade_1.append(manager.em_execucao)
                elif manager.em_execucao['prioridade'] == 2:
                    manager.prioridade_2.append(manager.em_execucao)
                elif manager.em_execucao['prioridade'] == 3:
                    manager.prioridade_3.append(manager.em_execucao)
                manager.em_execucao = {}
        #Avanca uma unidade de tempo
        t += 1

    #Mostra saida do sistema de arquivos
    logger.disco(filesystem)
if __name__ == '__main__':
    main()
