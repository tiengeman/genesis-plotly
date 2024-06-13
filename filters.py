import pandas as pd
from banco import *

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