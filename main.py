import memory_manager as mm
# import io_manager as iom
import file_manager as fm
import process_manager as pm
import operator


def main ():
    manager = pm.ProcessManager()
    memory = mm.MemoryManager()
    filesystem = fm.FileManager()
    with open('processes.txt', 'r') as f:
        procs = [[int(x) for x in line.split(',')] for line in f]
        processes = [pm.Process(x).__dict__ for x in procs]
    with open('files.txt', 'r') as f:
        temp = f.read().splitlines()
        filesystem.qtd_blocos = int(temp[0])
        filesystem.qtd_segmentos = int(temp[1])
        filesystem.arquivos = [fm.File(temp[i].split(',')).__dict__
                                for i in range(2, filesystem.qtd_segmentos+2)]
        filesystem.operacoes = [fm.FileOperation(temp[i].split(',')).__dict__
                                for i in range(filesystem.qtd_segmentos+3, len(temp))]

    import ipdb; ipdb.set_trace()
    # print processes
    manager.fila_principal = list(sorted(processes, key=operator.itemgetter('tempo_init')))
    # quantum
    t = 0
    # import ipdb; ipdb.set_trace()
    while(True):
        #Se tiver processo ainda nao processado
        while(manager.fila_principal):
            #Escalona processos do tempo de chegada = t
            if(manager.fila_principal[0]['tempo_init'] == t):
                manager.escalona_processo_geral()
            else:
                break
        #Escalona processos da fila de usuario
        while(manager.escalona_processo_usuario()):
            pass
        #SE NAO TEM NADA EXECUTANDO(SE TIVER VAI SER TEMPO REAL)
        if(not(manager.em_execucao)):
            #Executa tempo real se tiver
            if(manager.fila_tempo_real):
                offset = memory.salva(manager.fila_tempo_real[0])
                if(offset != None):
                    manager.em_execucao = manager.fila_tempo_real.pop(0)
                    manager.em_execucao['offset'] = offset

            #Processa execucao de usuario
            elif(manager.prioridade_1 or manager.prioridade_2 or manager.prioridade_3):
                # nao tem interrupcao
                if manager.prioridade_1:
                    if not(manager.prioridade_1[0]['offset']):
                        offset = memory.salva(manager.prioridade_1[0])
                    else:
                        offset = manager.prioridade_1[0]['offset']
                    if(offset != None):
                        manager.em_execucao = manager.prioridade_1.pop(0)
                        manager.em_execucao['offset'] = offset

                # para os processos de prioridade 2
                elif manager.prioridade_2:
                    if not(manager.prioridade_2[0]['offset']):
                        offset = memory.salva(manager.prioridade_2[0])
                    else:
                        offset = manager.prioridade_2[0]['offset']
                    if(offset != None):
                        manager.em_execucao = manager.prioridade_2.pop(0)
                        manager.em_execucao['offset'] = offset

                # para os processos de prioridade 3
                elif manager.prioridade_3:
                    if not(manager.prioridade_3[0]['offset']):
                        offset = memory.salva(manager.prioridade_3[0])
                    else:
                        offset = manager.prioridade_3[0]['offset']
                    if(offset != None):
                        manager.em_execucao = manager.prioridade_3.pop(0)
                        manager.em_execucao['offset'] = offset
            elif(not (manager.fila_principal)):
                break
        # OLHA A EXECUCAAAAAAO
        if(manager.em_execucao):
            print ('executando processo ',manager.em_execucao['PID'], manager.em_execucao['tempo_init'])
            manager.em_execucao['tempo_processador'] -= 1
            #APOS EXECUCAO
            #MATA SE TIVER ACABADO O TEMPO
            if manager.em_execucao['tempo_processador'] == 0:
                memory.mata(manager.em_execucao)
                manager.em_execucao = {}
            #REMOVE DO PROCESSADOR SE FOR DE USUARIO(ANDA A FILA)
            elif manager.em_execucao['prioridade'] > 0:
                if manager.em_execucao['prioridade'] == 1:
                    manager.prioridade_1.append(manager.em_execucao)
                elif manager.em_execucao['prioridade'] == 2:
                    manager.prioridade_2.append(manager.em_execucao)
                elif manager.em_execucao['prioridade'] == 3:
                    manager.prioridade_3.append(manager.em_execucao)
                manager.em_execucao = {}
        else:
            print 'stalled'
        t += 1

if __name__ == '__main__':
    main()
