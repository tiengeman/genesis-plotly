import pandas as pd
import back.queries

#cria o df para cada aba da planilha de dados
def receitas():
    df_receitas = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-receitas')
    return df_receitas

def despesasrel():
    df_despesasrel = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-despesasrel')
    return df_despesasrel

def despesasfin():
    df_despesasfin = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-despesasfin')
    return df_despesasfin

def despesasfol():
    df_despesasfol = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-despesasfol')
    return df_despesasfol

def filiais():
    df_filiais = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-filiais')
    return df_filiais

def projetos():
    df_projetos = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-projetos')
    return df_projetos

def premissas():
    df_premissas = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-premissas')
    return df_premissas

def orcamentos():
    df_orcamentos = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-orcamentos')
    return df_orcamentos

def impostos():
    df_impostos = pd.read_excel(r"C:\Users\eduardo.teles\Documents\genesis\tabelas sql (sistema custos).xlsx", sheet_name='cad-impostos')
    return df_impostos

def tabela(mes):
    lista_contrato, lista_soma_comp = back.queries.medicao(back.db, mes)
    list_cc = [None]*len(lista_contrato)
    list_local = [None]*len(lista_contrato)
    list_inativo = [None]*len(lista_contrato)
    list_filial = [None]*len(lista_contrato)
    list_despesas = [None]*len(lista_contrato)
    list_lucro = [None]*len(lista_contrato)
    list_perc = [None]*len(lista_contrato)
    list_medicao_total = [None]*len(lista_contrato)
    list_desp_totais = [None]*len(lista_contrato)
    list_lucro_total = [None]*len(lista_contrato)
    df = pd.DataFrame.from_dict(data={'LOCAL':list_local, 
                                      'CONTRATO':lista_contrato, 
                                      'C.CUSTOS':list_cc, 
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

def tabela_2():
    lista_remove_contrato = ["INVESTIMENTOS (CONTRATOS)", "EXPANSÃO - FILIAL MACAÉ", "EXPANSÃO - MATRIZ RECIFE", "DEPÓSITO JUDICIAIS", "ENGEMAN TECNOLOGIAS"]
    lista_remove_cc = ['888', '2180', '2250', '1111', '1930']
    list_local = [None]*len(lista_remove_contrato)
    list_inativo = [None]*len(lista_remove_contrato)
    list_filial = [None]*len(lista_remove_contrato)
    list_medicao = [None]*len(lista_remove_contrato)
    list_despesas = [None]*len(lista_remove_contrato)
    list_lucro = [None]*len(lista_remove_contrato)
    list_perc = [None]*len(lista_remove_contrato)
    list_medicao_total = [None]*len(lista_remove_contrato)
    list_desp_totais = [None]*len(lista_remove_contrato)
    list_lucro_total = [None]*len(lista_remove_contrato)
    df = pd.DataFrame.from_dict(data={'LOCAL':list_local, 
                                      'CONTRATO':lista_remove_contrato, 
                                      'C.CUSTOS':lista_remove_cc, 
                                      'INATIVO':list_inativo,
                                      'FILIAL':list_filial, 
                                      '(R) MEDIÇÃO':list_medicao, 
                                      '(D) DESPESAS':list_despesas, 
                                      '(R-D) LUCRO':list_lucro, 
                                      '%':list_perc,
                                      'MEDIÇÃO TOTAL': list_medicao_total,
                                      'DESPESAS TOTAIS': list_desp_totais,
                                      'LUCRO TOTAL': list_lucro_total})
    
    return df