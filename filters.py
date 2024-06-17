import pandas as pd
from banco import *
import back.queries
import back.banco_teste
from back.inserts import inserir_contrato

def filtra_detalha(df, selecao, contrato):
    if len(selecao) == 0 and len(contrato) == 0:
        return df
    elif len(selecao) == 0 and len(contrato) > 0:
        df_final = df[df['DESCRIÇÃO'].isin(contrato)]
        return df_final
    elif len(selecao) > 0 and len(contrato) == 0:
        df_final = df[df['COMPETENCIA'].isin(selecao)]
        return df_final
    elif len(selecao) > 0 and len(contrato) > 0:
        df_final = df[df['DESCRIÇÃO'].isin(contrato)]
        df_final = df_final[df_final['COMPETENCIA'].isin(selecao)]
        return df_final
    

def df_geral_tabela(mes):
    lista_todos_contrato, lista_todos_cc, lista_todos_locais = back.pega_centro_custos()
    lista_todos_contrato, lista_todos_cc, lista_todos_locais = ordenar_listas_locais(lista_todos_contrato, lista_todos_cc, lista_todos_locais)
    df_receita = detalha_receita_sem_format()
    df_receita = df_receita.fillna(0)
    df_despesa = detalha_despesas_sem_format()
    df_despesa = df_despesa.fillna(0)
    lista_medicao_comp = []
    lista_medicao_total = []
    lista_despesa_comp = []
    lista_despesa_total = []
    for i in lista_todos_cc:
        df_receita_filtrado = df_receita.query(f"PROJETOUNI == {i}")
        lista_medicao_total.append(sum(df_receita_filtrado['VALOR']))
        df_receita_filtrado = df_receita_filtrado.query(f'COMPETENCIA == "{mes}"')
        lista_medicao_comp.append(sum(df_receita_filtrado['VALOR']))

        df_despesa_filtrado = df_despesa.query(f"PROJETOUNI == {i}")
        lista_despesa_total.append(sum(df_despesa_filtrado['VALOR ORI']))
        df_despesa_filtrado = df_despesa_filtrado.query(f'COMPETENCIA == "{mes}"')
        lista_despesa_comp.append(sum(df_despesa_filtrado['VALOR ORI']))
    
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
    lista_lucro.append(lista_medicao_comp[-1]-lista_despesa_comp[-1])
    del lista_lucro_total[-1]
    lista_lucro_total.append(lista_medicao_total[-1]-lista_despesa_total[-1])

    lista_perc = perc(lista_medicao_comp, lista_lucro)
    lista_perc_total = perc(lista_medicao_total, lista_lucro_total)

    df = pd.DataFrame.from_dict(data={'LOCAL':lista_todos_locais, 
                                      'CONTRATO':lista_todos_contrato, 
                                      'C.CUSTOS':lista_todos_cc, 
                                      'INATIVO':lista_inativo,
                                      'FILIAL':[None]*len(lista_todos_cc), 
                                      'MEDIÇÃO':lista_medicao_comp, 
                                      'DESPESAS':lista_despesa_comp, 
                                      'LUCRO':lista_lucro, 
                                      '%':lista_perc,
                                      'MEDIÇÃO TOTAL': lista_medicao_total,
                                      'DESPESAS TOTAIS': lista_despesa_total,
                                      'LUCRO TOTAL': lista_lucro_total,
                                      '% TOTAL': lista_perc_total})
    
    return df
