import pandas as pd
import back.queries
import back.banco_teste

#cria o df para cada aba da planilha de dados
# def receitas():
#     df_receitas = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-receitas')
#     return df_receitas

# def despesasrel():
#     df_despesasrel = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-despesasrel')
#     return df_despesasrel

# def despesasfin():
#     df_despesasfin = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-despesasfin')
#     return df_despesasfin

# def despesasfol():
#     df_despesasfol = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-despesasfol')
#     return df_despesasfol

# def filiais():
#     df_filiais = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-filiais')
#     return df_filiais

# def projetos():
#     df_projetos = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-projetos')
#     return df_projetos

# def premissas():
#     df_premissas = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-premissas')
#     return df_premissas

# def orcamentos():
#     df_orcamentos = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-orcamentos')
#     return df_orcamentos

# def impostos():
#     df_impostos = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-impostos')
#     return df_impostos

def tabela(mes):
    lista_contrato, lista_soma_comp, lista_cc = back.medicao(mes)
    lista_total_contrato, lista_total_valor, lista_total_cc = back.medicao_total()
    list_local = [None]*len(lista_contrato)
    list_inativo = inativo(lista_soma_comp)
    list_filial = [None]*len(lista_contrato)
    tupla_despesas = back.total_despesa_competencia(mes)
    list_despesas = ordena_lista_despesa(lista_contrato, tupla_despesas)
    list_lucro = [None]*len(lista_contrato)
    list_perc = [None]*len(lista_contrato)
    list_medicao_total = [None]*len(lista_contrato)
    list_desp_totais = [None]*len(lista_contrato)
    list_lucro_total = [None]*len(lista_contrato)
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
                                      'LUCRO TOTAL': list_lucro_total})
    
    return df

def inativo(lista_valores): #função para criar a lista se o contrato está inativo ou não
    lista_inativo = []
    for i in lista_valores:
        if i == 0:
            lista_inativo.append("SIM")
        else:
            lista_inativo.append("NÃO")
        
    return lista_inativo

def ordena_lista_despesa(lista_contrato, lista_desp): #função para ordenar a lista de despesas de acordo com a lista de contratos
    lista_apoio = []
    for i in lista_contrato:
        flag = False
        for a in lista_desp:
            if a[0]==i:
                lista_apoio.append(a[1])
                flag = True
        if flag == False:
            lista_apoio.append(0)

    return lista_apoio