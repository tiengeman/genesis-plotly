import pandas as pd
import back.queries
import back.banco_teste
from back.inserts import inserir_contrato

def tabela(mes, df_receita, df_despesa, lista_todos_contrato, lista_todos_cc, lista_todos_locais): 
    lista_medicao_comp = []
    lista_medicao_total = []
    lista_despesa_comp = []
    lista_despesa_total = []
    
    for i in lista_todos_cc:
        df_receita_filtrado = df_receita[df_receita['PROJETOUNI'] == i]
        lista_medicao_total.append(df_receita_filtrado['VALOR'].sum())
        
        df_receita_filtrado_comp = df_receita_filtrado[df_receita_filtrado['COMPETENCIA'] == mes]
        lista_medicao_comp.append(df_receita_filtrado_comp['VALOR'].sum())

        df_despesa_filtrado = df_despesa[df_despesa['PROJETOUNI'] == i]
        lista_despesa_total.append(df_despesa_filtrado['VALOR DESP'].sum())
        
        df_despesa_filtrado_comp = df_despesa_filtrado[df_despesa_filtrado['COMPETENCIA'] == mes]
        lista_despesa_comp.append(df_despesa_filtrado_comp['VALOR DESP'].sum())
    
    lista_todos_contrato.append("TOTAL OPERAÇÃO")
    lista_todos_locais.append("")
    lista_todos_cc.append("")
    
    lista_medicao_comp.append(sum_medicao(lista_todos_contrato, lista_medicao_comp))
    lista_medicao_total.append(sum_medicao(lista_todos_contrato, lista_medicao_total))
    lista_despesa_comp.append(sum_despesa(lista_todos_contrato, lista_despesa_comp))
    lista_despesa_total.append(sum_despesa(lista_todos_contrato, lista_despesa_total))

    lista_lucro = subtrair_listas(lista_medicao_comp, lista_despesa_comp)
    lista_lucro_total = subtrair_listas(lista_medicao_total, lista_despesa_total)
    lista_inativo = inativo(lista_lucro)

    del lista_inativo[-1]
    lista_inativo.append('NÃO')
    del lista_lucro[-1]
    lista_lucro.append(lista_medicao_comp[-1] - lista_despesa_comp[-1])
    del lista_lucro_total[-1]
    lista_lucro_total.append(lista_medicao_total[-1] - lista_despesa_total[-1])

    lista_perc = perc(lista_medicao_comp, lista_lucro)
    lista_perc_total = perc(lista_medicao_total, lista_lucro_total)

    df = pd.DataFrame.from_dict(data={'LOCAL': lista_todos_locais, 
                                      'CONTRATO': lista_todos_contrato, 
                                      'C.CUSTOS': lista_todos_cc, 
                                      'INATIVO': lista_inativo,
                                      'FILIAL': [None] * len(lista_todos_cc), 
                                      'MEDIÇÃO': lista_medicao_comp, 
                                      'DESPESAS': lista_despesa_comp, 
                                      'LUCRO': lista_lucro, 
                                      '%': lista_perc,
                                      'MEDIÇÃO TOTAL': lista_medicao_total,
                                      'DESPESAS TOTAIS': lista_despesa_total,
                                      'LUCRO TOTAL': lista_lucro_total,
                                      '% TOTAL': lista_perc_total})
    
    return df
# tabela do capex
def tabela_2(mes):
    lista_contrato = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    lista_contrato.append('TOTAL CAPEX')
    list_local = ['CAPEX']*(len(lista_contrato)-1)
    list_local.append("")
    lista_cc = [888, 2180, 2250, 1111, 1930, ""]
    list_inativo = [None]*len(lista_contrato)
    del list_inativo[-1]
    list_inativo.append("NÂO")
    list_filial = [None]*len(lista_contrato)
    lista_soma_comp = medicao_capex(mes)
    lista_soma_comp.append(sum(lista_soma_comp))
    tupla_despesas = back.total_despesa_competencia(mes) #gera uma lista de tuplas com as info
    list_despesas = ordena_lista(lista_cc, tupla_despesas) #aqui ele ordena os valores de acordo com a lista de contrato
    del list_despesas[-1]
    list_despesas.append(sum(list_despesas))
    list_lucro = subtrair_listas(lista_soma_comp, list_despesas)
    list_perc = list_perc = perc(lista_soma_comp, list_lucro)
    list_medicao_total = medicao_capex_total()
    list_medicao_total.append(sum(list_medicao_total))
    tupla_despesa_total = back.total_despesa()
    list_desp_totais = ordena_lista(lista_cc, tupla_despesa_total)
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
            soma += float(lista_soma_comp[i])
    return soma

def sum_despesa(lista_contrato_final, lista_despesas): # cria o somatorio da despesa
    soma = 0
    for i in range(len(lista_despesas)):
        if lista_contrato_final[i] != "ADM LOCAL (MACAÉ)" and lista_contrato_final[i] != "FILIAL - PERNAMBUCO (RECIFE)":
            soma += lista_despesas[i]
    return soma

def ordenar_listas_locais(lista_contrato, lista_cc, lista_locais):
    # lista_todos_contrato, lista_todos_cc, lista_todos_locais = back.pega_centro_custos()
    
    # for i in range(len(lista_todos_contrato)):
    #     if lista_todos_cc[i] not in lista_cc:
    #         lista_contrato.append(lista_todos_contrato[i])
    #         lista_soma_comp.append(0)
    #         lista_cc.append(lista_todos_cc[i])
    #         lista_locais.append(lista_todos_locais[i])

    # Combine as listas em uma lista de tuplas
    combinados = list(zip(lista_contrato, lista_cc, lista_locais))

    # Ordene a lista primeiro por lista_locais em ordem crescente
    # e dentro de cada grupo de lista_locais por lista_contrato em ordem decrescente (ordem lexicográfica)
    combinados.sort(key=lambda x: (x[2], x[0]), reverse=True)
    combinados.sort(key=lambda x: x[2])

    # Descompacte as listas ordenadas de volta em suas listas originais
    lista_contrato, lista_cc, lista_locais = zip(*combinados)

    # Retorne as listas como tuplas
    return list(lista_contrato), list(lista_cc), list(lista_locais)

def inativo(lista_valores): #função para criar a lista se o contrato está inativo ou não
    lista_inativo = []
    for i in lista_valores:
        if i == 0:
            lista_inativo.append("SIM")
        else:
            lista_inativo.append("NÃO")
        
    return lista_inativo

def ordena_lista(lista_cc, lista_desp): #função para ordenar a lista de despesas de acordo com a lista de contratos
    lista_apoio = []                        # a lista de valores devem ser tuplas
    for i in lista_cc:
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
    lista_capex = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS', 'CUSTOS DIRETORIA']
    list_index = []
    for i in lista_capex:
        if i in lista_contratos:
            index = lista_contratos.index(i)
            del lista_contratos[index]
            del lista_valor[index]
            del lista_cc[index]
            del list_locais[index]
    
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

def detalha_despesas():
    lista_desp = back.detalha_despesas()
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

def detalha_receita():

    lista_receita = back.detalha_receita()
    nome_colunas = ['ID', 'PROJETO-UNI', 'DESCRIÇÃO', 'PROJETO-ORI', 'DOCUMENTO', 'CLIENTE', 'DATA', 'VALOR', 'VALOR-RETENCAO', 'VALOR-ADM', 'COMPETENCIA', 'FILIAL']
    dicionario_de_listas = {coluna: [] for coluna in nome_colunas}
    for linha in lista_receita:
        for i, valor in enumerate(linha):
            dicionario_de_listas[nome_colunas[i]].append(valor)
    del dicionario_de_listas['ID']
    df_receita = pd.DataFrame.from_dict(data=dicionario_de_listas)
    format_numeric_columns(df_receita, ["VALOR"])
    
    return df_receita

def detalha_receita_sem_format():

    lista_receita = back.detalha_receita()
    nome_colunas = ['ID', 'PROJETOUNI', 'DESCRIÇÃO', 'PROJETO-ORI', 'DOCUMENTO', 'CLIENTE', 'DATA', 'VALOR', 'VALOR-RETENCAO', 'VALOR-ADM', 'COMPETENCIA', 'FILIAL']
    dicionario_de_listas = {coluna: [] for coluna in nome_colunas}
    for linha in lista_receita:
        for i, valor in enumerate(linha):
            dicionario_de_listas[nome_colunas[i]].append(valor)
    del dicionario_de_listas['ID']
    df_receita = pd.DataFrame.from_dict(data=dicionario_de_listas)
    
    return df_receita

def detalha_despesas_sem_format():
    lista_desp = back.detalha_despesas()
    nome_colunas = ['ID', 'PROJETOUNI', 'DESCRIÇÃO', 'PROJETO-ORI', 'DOCUMENTO', 'AGENTE', 'DESC. AGENTE', 'VALOR ORI', 'VALOR INVEST.', 'VALOR DESP', 'COD. CLASSE', 'DESC. CLASSE', 'DATA', 'COMPETENCIA', 'CATEGORIA',
                    'OBSERVAÇÕES', 'TIPO']
    dicionario_de_listas = {coluna: [] for coluna in nome_colunas}
    for linha in lista_desp:
        for i, valor in enumerate(linha):
            dicionario_de_listas[nome_colunas[i]].append(valor)
    del dicionario_de_listas['ID']
    df_impostos = pd.DataFrame.from_dict(data=dicionario_de_listas)

    return df_impostos