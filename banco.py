import pandas as pd
import back.queries
import back.banco_teste
from back.inserts import inserir_contrato

def tabela(mes): #função que gera a tabela principal da aba gerencial
    lista_contrato, lista_soma_comp, lista_cc, lista_locais = back.medicao(mes)
    lista_contrato, lista_soma_comp, lista_cc, lista_locais = ordenar_listas_locais(lista_contrato, lista_soma_comp, lista_cc, lista_locais)
    lista_locais.append("")
    lista_contrato.append('TOTAL OPERAÇÃO')
    lista_contrato_final, lista_soma_comp, lista_cc, lista_locais = remove_capex(lista_contrato, lista_soma_comp, lista_cc, lista_locais)
    lista_cc.append('')
    lista_soma_comp.append(sum_medicao(lista_contrato_final, lista_soma_comp))
    lista_cont_total, lista_valor_total, lista_cc_total = back.medicao_total()
    tupla_medicao_total = merge_lists_into_tuples(lista_cont_total, lista_valor_total)
    tupla_despesa_total = back.total_despesa()
    tupla_despesas = back.total_despesa_competencia(mes) #gera uma lista de tuplas com as info

    list_filial = [None]*len(lista_contrato_final)
    list_despesas = ordena_lista(lista_contrato_final, tupla_despesas) #aqui ele ordena os valores de acordo com a lista de contrato
    del list_despesas[-1]
    list_despesas.append(sum_despesa(lista_contrato_final, list_despesas))
    list_lucro = subtrair_listas(lista_soma_comp, list_despesas)
    del list_lucro[-1]
    list_lucro.append(lista_soma_comp[-1]-list_despesas[-1])
    list_perc = perc(lista_soma_comp, list_lucro)
    list_medicao_total = ordena_lista(lista_contrato_final, tupla_medicao_total)
    del list_medicao_total[-1]
    list_medicao_total.append(sum_medicao(lista_contrato_final, list_medicao_total))
    list_desp_totais = ordena_lista(lista_contrato_final, tupla_despesa_total)
    del list_desp_totais[-1]
    list_desp_totais.append(sum_despesa(lista_contrato_final, list_desp_totais))
    list_lucro_total = subtrair_listas(list_medicao_total, list_desp_totais)
    del list_lucro_total[-1]
    list_lucro_total.append(list_medicao_total[-1]-list_desp_totais[-1])
    list_perc_total = perc(list_medicao_total, list_lucro_total)
    list_inativo = inativo(list_lucro) #gera a lista se é inativo ou não
    del list_inativo[-1]
    list_inativo.append('NÃO')
    df = pd.DataFrame.from_dict(data={'LOCAL':lista_locais, 
                                      'CONTRATO':lista_contrato_final, 
                                      'C.CUSTOS':lista_cc, 
                                      'INATIVO':list_inativo,
                                      'FILIAL':list_filial, 
                                      'MEDIÇÃO':lista_soma_comp, 
                                      'DESPESAS':list_despesas, 
                                      'LUCRO':list_lucro, 
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
                                      'MEDIÇÃO':lista_soma_comp, 
                                      'DESPESAS':list_despesas, 
                                      'LUCRO':list_lucro, 
                                      '%':list_perc,
                                      'MEDIÇÃO TOTAL': list_medicao_total,
                                      'DESPESAS TOTAIS': list_desp_totais,
                                      'LUCRO TOTAL': list_lucro_total,
                                      '% TOTAL': list_perc_total})
    
    return df

def sum_medicao(lista_contrato_final, lista_soma_comp): #cria o somatório da medicao
    soma = 0
    for i in range(len(lista_soma_comp)):
        if lista_contrato_final[i] != "ADM CENTRAL (RECIFE)":
            soma += lista_soma_comp[i]
    return soma

def sum_despesa(lista_contrato_final, lista_despesas): # cria o somatorio da despesa
    soma = 0
    for i in range(len(lista_despesas)):
        if lista_contrato_final[i] != "ADM LOCAL (MACAÉ)" and lista_contrato_final[i] != "FILIAL - PERNAMBUCO (RECIFE)":
            soma += lista_despesas[i]
    return soma

def ordenar_listas_locais(lista_contrato, lista_soma_comp, lista_cc, lista_locais):
    # Garantir que todas as listas têm o mesmo comprimento
    if not (len(lista_contrato) == len(lista_soma_comp) == len(lista_cc) == len(lista_locais)):
        raise ValueError("Todas as listas devem ter o mesmo comprimento")
    
    lista_todos_contrato, lista_todos_cc, lista_todos_locais = back.pega_centro_custos()
    for i in range(len(lista_todos_contrato)):
        if lista_todos_contrato[i] not in lista_contrato:
            lista_contrato.append(lista_todos_contrato[i])
            lista_soma_comp.append(0)
            lista_cc.append(lista_todos_cc[i])
            lista_locais.append(lista_todos_locais[i])

    # Convertendo todos os elementos de lista_locais para strings e lista_cc para inteiros
    lista_locais_str = list(map(str, lista_locais))
    lista_cc_int = list(map(int, lista_cc))
    
    # Cria uma lista de tuplas que combina todas as listas
    combined_list = list(zip(lista_locais_str, lista_cc_int, lista_soma_comp, lista_contrato))
    
    # Ordena primeiro pelos locais (decrescente) e depois pelos cc (crescente)
    combined_list_sorted = sorted(combined_list, key=lambda x: (-ord(x[0][0]), x[1]))
    
    # Separa as listas ordenadas

    lista_locais_ordenada, lista_cc_ordenada, lista_soma_comp_ordenada, lista_contrato_ordenada = zip(*combined_list_sorted)
    
    return list(lista_contrato_ordenada), list(lista_soma_comp_ordenada), list(lista_cc_ordenada), list(lista_locais_ordenada)

def inativo(lista_valores): #função para criar a lista se o contrato está inativo ou não
    lista_inativo = []
    for i in lista_valores:
        if i == 0:
            lista_inativo.append("SIM")
        else:
            lista_inativo.append("NÃO")
        
    return lista_inativo

def ordena_lista(lista_contrato, lista_desp): #função para ordenar a lista de despesas de acordo com a lista de contratos
    lista_apoio = []
    print(lista_desp)                           # a lista de valores devem ser tuplas
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
    lista_contrato, lista_soma_comp, lista_cc, lista_locais = back.medicao(mes)
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

def remove_capex(lista_contratos, lista_valor, lista_cc, list_locais): #função para gerar uma lista sem o capex
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
        del list_locais[i]
    
    return lista_contratos, lista_valor, lista_cc, list_locais

def df_impostos(): # forma o df com os impostos
    lista_contrato, lista_impostos = back.impostos()
    df = pd.DataFrame.from_dict(data={'CONTRATO': lista_contrato,
                                      'IMPOSTO': lista_impostos})
    return df

def format_numeric_columns(df, columns): # formata as colunas no formato de moeda
    for col in columns:
        # Aplica a formatação para cada valor na coluna
        df[col] = df[col].apply(lambda x: '{:,.2f}'.format(x).replace('.', '*').replace(',', '.').replace('*', ','))

def cad_contratos():
    lista = back.cad_contratos()
    nome_colunas = ['ID', 'OS', 'TIPO', 'ENQUADRAMENTO', 'CLIENTE', 'DESC', 'ICJ', 'SAP', 'INICIO', 'FIM', 'ADITIVOS', 'VALOR', 'PRAZOMES', 'PRAZODIAS', 'STATUS', 'RESPONSAVEL', 'FILIAL',
                    'PROJETO', 'PROJETOSAPIENS', 'ISS', 'ADMCENTRAL', 'PIS', 'COFINS', 'CSLL', 'IRPJ', "INVESTIMENTOS", 'ICMS']
    dicionario_de_listas = {coluna: [] for coluna in nome_colunas}
    for linha in lista:
        for i, valor in enumerate(linha):
            dicionario_de_listas[nome_colunas[i]].append(valor)
    del dicionario_de_listas['ID']
    df_contratos = pd.DataFrame.from_dict(data=dicionario_de_listas)

    return df_contratos

def cad_impostos():
    lista = back.cad_impostos()
    nome_colunas = ['ID', 'RECEITATOTAL', 'PISRETIDO', 'PISPAGO', 'COFINSRETIDO', 'COFINSPAGO', 'DATA FECHAMENTO', 'COMPETENCIA']
    dicionario_de_listas = {coluna: [] for coluna in nome_colunas}
    for linha in lista:
        for i, valor in enumerate(linha):
            dicionario_de_listas[nome_colunas[i]].append(valor)
    del dicionario_de_listas['ID']
    df_impostos = pd.DataFrame.from_dict(data=dicionario_de_listas)
    format_numeric_columns(df_impostos, ["RECEITATOTAL", 'PISRETIDO', 'PISPAGO', 'COFINSRETIDO', 'COFINSPAGO'])

    return df_impostos

def cad_encargos():
    lista_encargos = back.cad_encargos()
    lista = []
    nome_colunas = ['id', 'CODIGO', 'NOME', 'CNPJ', 'PERCENTUAL', 'CPRB', 'INICIO', 'FIM']
    for a in lista_encargos:
        dicionario_de_listas = {coluna: [] for coluna in nome_colunas}
        for linha in a:
            for i, valor in enumerate(linha):
                dicionario_de_listas[nome_colunas[i]].append(valor)
        del dicionario_de_listas['id']
        df_encargos = pd.DataFrame.from_dict(data=dicionario_de_listas)
        lista.append(df_encargos)
    return lista
    
def enviar_contratos(lista):
    try:
        inserir_contrato(lista)
        return "Cadastro realizado com sucesso"
    except Exception as e:
        return str(e)
    
def lista_contratos():
    lista_contrato, lista_soma_comp, lista_cc = back.medicao_total()
    
    return lista_contrato

def detalha_despesas(competencia, contrato):
    lista_desp = back.detalha_despesas(competencia, contrato)
    nome_colunas = ['ID', 'PROJETO-UNI', 'DESCRIÇÃO', 'PROJETO-ORI', 'DOCUMENTO', 'AGENTE', 'DESC. AGENTE', 'VALOR ORI', 'VALOR INVEST.', 'VALOR DESP', 'COD. CLASSE', 'DESC. CLASSE', 'DATA', 'COMPETENCIA', 'CATEGORIA',
                    'OBSERVAÇÕES', 'TIPO']
    dicionario_de_listas = {coluna: [] for coluna in nome_colunas}
    for linha in lista_desp:
        for i, valor in enumerate(linha):
            dicionario_de_listas[nome_colunas[i]].append(valor)
    del dicionario_de_listas['ID']
    df_impostos = pd.DataFrame.from_dict(data=dicionario_de_listas)
    format_numeric_columns(df_impostos, ['VALOR ORI', 'VALOR DESP'])

    return df_impostos

def detalha_receita(competencia, contrato):

    lista_receita = back.detalha_receita(competencia, contrato)
    nome_colunas = ['ID', 'PROJETO-UNI', 'DESCRIÇÃO', 'PROJETO-ORI', 'DOCUMENTO', 'CLIENTE', 'DATA', 'VALOR', 'VALOR-RETENCAO', 'VALOR-ADM', 'COMPETENCIA', 'FILIAL']
    dicionario_de_listas = {coluna: [] for coluna in nome_colunas}
    for linha in lista_receita:
        for i, valor in enumerate(linha):
            dicionario_de_listas[nome_colunas[i]].append(valor)
    del dicionario_de_listas['ID']
    df_receita = pd.DataFrame.from_dict(data=dicionario_de_listas)
    format_numeric_columns(df_receita, ["VALOR"])
    
    return df_receita