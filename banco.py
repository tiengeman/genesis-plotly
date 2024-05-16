import pandas as pd
import back.queries
import back.banco_teste

def tabela(mes): #função que gera a tabela principal da aba gerencial
    lista_contrato, lista_soma_comp, lista_cc = back.medicao(mes)
    lista_contrato.append('TOTAL OPERAÇÃO')
    lista_contrato_final, lista_soma_comp, lista_cc = remove_capex(lista_contrato, lista_soma_comp, lista_cc)
    lista_cc.append('')
    lista_soma_comp.append(sum(lista_soma_comp))
    lista_cont_total, lista_valor_total, lista_cc_total = back.medicao_total()
    tupla_medicao_total = merge_lists_into_tuples(lista_cont_total, lista_valor_total)
    tupla_despesa_total = back.total_despesa()
    tupla_despesas = back.total_despesa_competencia(mes) #gera uma lista de tuplas com as info

    list_local = [None]*len(lista_contrato_final)
    list_inativo = inativo(lista_soma_comp) #gera a lista se é inativo ou não
    del list_inativo[-1]
    list_inativo.append('NÃO')
    list_filial = [None]*len(lista_contrato_final)
    list_despesas = ordena_lista(lista_contrato_final, tupla_despesas) #aqui ele ordena os valores de acordo com a lista de contrato
    del list_despesas[-1]
    list_despesas.append(sum(list_despesas))
    list_lucro = subtrair_listas(lista_soma_comp, list_despesas)
    del list_lucro[-1]
    list_lucro.append(sum(list_lucro))
    list_perc = perc(lista_soma_comp, list_lucro)
    list_medicao_total = ordena_lista(lista_contrato_final, tupla_medicao_total)
    del list_medicao_total[-1]
    list_medicao_total.append(sum(list_medicao_total))
    list_desp_totais = ordena_lista(lista_contrato_final, tupla_despesa_total)
    del list_desp_totais[-1]
    list_desp_totais.append(sum(list_desp_totais))
    list_lucro_total = subtrair_listas(list_medicao_total, list_desp_totais)
    del list_lucro_total[-1]
    list_lucro_total.append(sum(list_lucro_total))
    list_perc_total = perc(list_medicao_total, list_lucro_total)
    df = pd.DataFrame.from_dict(data={'LOCAL':list_local, 
                                      'CONTRATO':lista_contrato_final, 
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

# tabela do capex
def tabela_2(mes):
    lista_contrato = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    lista_contrato.append('TOTAL CAPEX')
    list_local = ['CAPEX']*(len(lista_contrato)-1)
    list_local.append("")
    lista_cc = ['888', '2180', '2250', '1111', '1930', ""]
    list_inativo = [None]*len(lista_contrato)
    del list_inativo[-1]
    list_inativo.append("NÂO")
    list_filial = [None]*len(lista_contrato)
    lista_soma_comp = medicao_capex(mes)
    lista_soma_comp.append(sum(lista_soma_comp))
    tupla_despesas = back.total_despesa_competencia(mes) #gera uma lista de tuplas com as info
    list_despesas = ordena_lista(lista_contrato, tupla_despesas) #aqui ele ordena os valores de acordo com a lista de contrato
    del list_despesas[-1]
    list_despesas.append(sum(list_despesas))
    list_lucro = subtrair_listas(lista_soma_comp, list_despesas)
    list_perc = list_perc = perc(lista_soma_comp, list_lucro)
    list_medicao_total = medicao_capex_total()
    list_medicao_total.append(sum(list_medicao_total))
    tupla_despesa_total = back.total_despesa()
    list_desp_totais = ordena_lista(lista_contrato, tupla_despesa_total)
    del list_desp_totais[-1]
    list_desp_totais.append(sum(list_desp_totais))
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

def medicao_capex(mes): # gera a coluna de medição para o capex
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
        
def medicao_capex_total(): # gera a coluna de medição total para o capex
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

def remove_capex(lista_contratos, lista_valor, lista_cc): #função para gerar uma lista sem o capex
    lista_capex = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    list_index = []
    for i in lista_capex:
        for a in range(len(lista_contratos)):
            if i == lista_contratos[a]:
                list_index.append(a)
    for i in list_index:
        del lista_contratos[i]
        del lista_valor[i]
        del lista_cc[i]
    
    return lista_contratos, lista_valor, lista_cc

def df_impostos(): # forma o df com os impostos
    lista_contrato, lista_impostos = back.impostos()
    df = pd.DataFrame.from_dict(data={'CONTRATO': lista_contrato,
                                      'IMPOSTO': lista_impostos})
    return df

def format_numeric_columns(df, columns): # formata as colunas no formato de moeda
    for col in columns:
        # Aplica a formatação para cada valor na coluna
        df[col] = df[col].apply(lambda x: '{:,.2f}'.format(x).replace('.', '*').replace(',', '.').replace('*', ','))