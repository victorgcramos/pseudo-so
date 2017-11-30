import memory_manager as mm
# import io_manager as iom
# import file_manager as fm
import process_manager as pm
import operator


def main ():
    with open('processes.txt', 'r') as f:
        procs = [[int(x) for x in line.split(',')] for line in f]
        processes = [pm.Process(x).__dict__ for x in procs]
    # print processes
    manager = pm.ProcessManager()
    memory = mm.MemoryManager()
    manager.fila_principal = list(sorted(processes, key=operator.itemgetter('tempo_init')))

    # quantum
    t = 0
    while(True):
        #Se tiver processo ainda nao processado
        if(manager.fila_principal):
            #Escalona processos do tempo de chegada = t
            while(manager.fila_principal[0]['tempo_init'] == t):
                manager.escalona_processo_geral()
            #Escalona processos da fila de usuario
            while(manager.fila_usuario):
                manager.escalona_processo_usuario()
        #Executa tempo real se tiver

        if(manager.fila_tempo_real):
            print 'tempo_real'
            if(manager.em_execucao):
                if(manager.em_execucao['prioridade'] > 0):
                    #INTERROMPE
                    offset = memory.salva(manager.fila_tempo_real[0])
                    if(offset != None):
                        manager.em_execucao = manager.fila_tempo_real.pop(0)
                        manager.em_execucao['offset'] = offset

            else:
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
        else:
            break
        # OLHA A EXECUCAAAAAAO
        manager.em_execucao['tempo_processador'] -= 1
        if manager.em_execucao['tempo_processador'] == 0:
            memory.mata(manager.em_execucao)
        t += 1

if __name__ == '__main__':
    main()
