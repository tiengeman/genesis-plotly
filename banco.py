import pandas as pd
import back.queries
import back.banco_teste

def tabela(mes): #função que gera a tabela principal do resumo
    lista_contrato, lista_soma_comp, lista_cc = back.medicao(mes)
    lista_contrato.append('TOTAL OPERAÇÃO')
    lista_cc.append('')
    lista_soma_comp.append(sum(lista_soma_comp))
    lista_cont_total, lista_valor_total, lista_cc_total = back.medicao_total()
    tupla_medicao_total = merge_lists_into_tuples(lista_cont_total, lista_valor_total)
    tupla_despesa_total = back.total_despesa()
    tupla_despesas = back.total_despesa_competencia(mes) #gera uma lista de tuplas com as info

    list_local = [None]*len(lista_contrato)
    list_inativo = inativo(lista_soma_comp) #gera a lista se é inativo ou não
    del list_inativo[-1]
    list_inativo.append('')
    list_filial = [None]*len(lista_contrato)
    list_despesas = ordena_lista(lista_contrato, tupla_despesas) #aqui ele ordena os valores de acordo com a lista de contrato
    del list_despesas[-1]
    list_despesas.append(sum(list_despesas))
    list_lucro = subtrair_listas(lista_soma_comp, list_despesas)
    del list_lucro[-1]
    list_lucro.append(sum(list_lucro))
    list_perc = perc(lista_soma_comp, list_lucro)
    list_medicao_total = ordena_lista(lista_contrato, tupla_medicao_total)
    del list_medicao_total[-1]
    list_medicao_total.append(sum(list_medicao_total))
    list_desp_totais = ordena_lista(lista_contrato, tupla_despesa_total)
    del list_desp_totais[-1]
    list_desp_totais.append(sum(list_desp_totais))
    list_lucro_total = subtrair_listas(list_medicao_total, list_desp_totais)
    del list_lucro_total[-1]
    list_lucro_total.append(sum(list_lucro_total))
    list_perc_total = perc(list_medicao_total, list_lucro_total)
    df = pd.DataFrame.from_dict(data={'LOCAL':list_local, 
                                      'CONTRATO':lista_contrato, 
                                      'C.CUSTOS':lista_cc, 
                                      'INATIVO':list_inativo,
                                      'FILIAL':list_filial, 
                                      '(R) MEDIÇÃO':lista_soma_comp, 
                                      '(D) DESPESAS':list_despesas, 
                                      '(R-D) LUCRO':list_lucro, 
                                      '%':list_perc,
                                      'MEDIÇÃO TOTAL': list_medicao_total,
                                      'DESPESAS TOTAIS': list_desp_totais,
                                      'LUCRO TOTAL': list_lucro_total,
                                      '% TOTAL': list_perc_total})
    
    return df

def tabela_2(mes):
    lista_contrato = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    list_local = ['CAPEX']*len(lista_contrato)
    lista_cc = ['888', '2180', '2250', '1111', '1930']
    list_inativo = [None]*len(lista_contrato)
    list_filial = [None]*len(lista_contrato)
    lista_soma_comp = medicao_capex(mes)
    tupla_despesas = back.total_despesa_competencia(mes) #gera uma lista de tuplas com as info
    list_despesas = ordena_lista(lista_contrato, tupla_despesas) #aqui ele ordena os valores de acordo com a lista de contrato
    list_lucro = subtrair_listas(lista_soma_comp, list_despesas)
    list_perc = list_perc = perc(lista_soma_comp, list_lucro)
    list_medicao_total = medicao_capex_total()
    tupla_despesa_total = back.total_despesa()
    list_desp_totais = ordena_lista(lista_contrato, tupla_despesa_total)
    list_lucro_total = subtrair_listas(list_medicao_total, list_desp_totais)
    list_perc_total = perc(list_medicao_total, list_lucro_total)
    df = pd.DataFrame.from_dict(data={'LOCAL':list_local, 
                                      'CONTRATO':lista_contrato, 
                                      'C.CUSTOS':lista_cc, 
                                      'INATIVO':list_inativo,
                                      'FILIAL':list_filial, 
                                      '(R) MEDIÇÃO':lista_soma_comp, 
                                      '(D) DESPESAS':list_despesas, 
                                      '(R-D) LUCRO':list_lucro, 
                                      '%':list_perc,
                                      'MEDIÇÃO TOTAL': list_medicao_total,
                                      'DESPESAS TOTAIS': list_desp_totais,
                                      'LUCRO TOTAL': list_lucro_total,
                                      '% TOTAL': list_perc_total})
    
    return df

def inativo(lista_valores): #função para criar a lista se o contrato está inativo ou não
    lista_inativo = []
    for i in lista_valores:
        if i == 0:
            lista_inativo.append("SIM")
        else:
            lista_inativo.append("NÃO")
        
    return lista_inativo

def ordena_lista(lista_contrato, lista_desp): #função para ordenar a lista de despesas de acordo com a lista de contratos
    lista_apoio = []                           # a lista de valores devem ser tuplas
    for i in lista_contrato:
        flag = False
        for a in lista_desp:
            if a[0]==i:
                lista_apoio.append(a[1])
                flag = True
        if flag == False:
            lista_apoio.append(0)

    return lista_apoio

def subtrair_listas(lista1, lista2): #calcula o lucro
    # Verifica se as listas têm o mesmo comprimento
    if len(lista1) != len(lista2):
        return "As listas precisam ter o mesmo comprimento!"
    resultado = []
    for i in range(len(lista1)):
        resultado.append(lista1[i] - lista2[i])
    
    return list(resultado)

def perc(lista_soma_comp, list_lucro): #função que retorna a lista com o calculo do percentual
    lista_perc = []
    for i in range(len(lista_soma_comp)):
        if lista_soma_comp[i] <= 0:
            lista_perc.append('-')
        else:
            lista_perc.append(list_lucro[i] / lista_soma_comp[i])
        
    return lista_perc

def merge_lists_into_tuples(list1, list2): #função para juntar duas listas e formar uma lista de tuplas
    # Verificar se ambas as listas têm o mesmo comprimento
    if len(list1) != len(list2):
        raise ValueError("As listas devem ter o mesmo comprimento.")

    # Usar zip para combinar as listas em uma lista de tuplas
    merged_list = list(zip(list1, list2))
    return merged_list

def medicao_capex(mes):
    lista_capex = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    medicao = []
    lista_contrato, lista_soma_comp, lista_cc = back.medicao(mes)
    for i in lista_capex:
        flag = False
        for a in range(len(lista_contrato)):
            if i == lista_contrato[a]:
                medicao.append(lista_soma_comp[a])
                flag = True
        if flag == False:
            medicao.append(0)

    return medicao
        
def medicao_capex_total():
    lista_capex = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    medicao_total = []
    lista_cont_total, lista_valor_total, lista_cc_total = back.medicao_total()
    for i in lista_capex:
        flag = False
        for a in range(len(lista_cont_total)):
            if i == lista_cont_total[a]:
                medicao_total.append(lista_valor_total[a])
                flag = True
        if flag == False:
            medicao_total.append(0)

    return medicao_total