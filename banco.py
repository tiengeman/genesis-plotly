import pandas as pd

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

def tabela():
    list_contratos = list(projetos()['descricao-projeto'])
    list_cc = list(projetos()['codigo-projeto'])
    list_local = [None]*len(list_contratos)
    list_inativo = [None]*len(list_contratos)
    list_filial = [None]*len(list_contratos)
    list_medicao = [None]*len(list_contratos)
    list_despesas = [None]*len(list_contratos)
    list_lucro = [None]*len(list_contratos)
    list_perc = [None]*len(list_contratos)
    df = pd.DataFrame.from_dict(data={'LOCAL':list_local, 
                                      'CONTRATO':list_contratos, 
                                      'C.CUSTOS':list_cc, 
                                      'INATIVO':list_inativo,
                                      'FILIAL':list_filial, 
                                      '(R) MEDIÇÃO':list_medicao, 
                                      '(D) DESPESAS':list_despesas, 
                                      '(R-D) LUCRO':list_lucro, 
                                      '%':list_perc})
    
    return df
