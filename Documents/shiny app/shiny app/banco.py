import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(filename='keys.json',
                                                                    scopes=["https://www.googleapis.com/auth/cloud-platform"])

def lista_centro_custo(credentials=credentials):
    query_cc = """SELECT DISTINCT string_field_0 FROM `custos-404821.Geral.cad-receitas3` WHERE string_field_0 IS NOT NULL"""
    lista = pd.read_gbq(query_cc, credentials=credentials)
    lista_cc = list(lista['string_field_0'])
    lista_cc.remove('PINTURA"')
    lista_cc.remove("R$ 6.340")
    lista_cc.remove("R$ 11.109")
    lista_cc.remove("R$ 16.062")
    lista_cc.remove("R$ 34.683")
    lista_cc.remove("R$ 35.721")
    lista_cc.remove("R$ 62.538")
    lista_cc.remove('SUPERVISOR "')
    lista_cc.remove('PINTOR OFFSHORE"')
    lista_cc.remove('Caldeiraria e Solda"')
    lista_cc.remove('SERVIÇO TEC. SEGURANÇA"')

    return lista_cc

def medidofaturado(cc, credentials=credentials):
    columns = ['CONTRATO', 'COMPETENCIA', 'MEDIDO', 'FATURADO']
    query = f"""SELECT string_field_1, string_field_4, string_field_7, string_field_20
                FROM 
                `custos-404821.Geral.cad-receitas3` WHERE string_field_0 = '{cc}'"""

    df = pd.read_gbq(query, credentials=credentials)
    df.columns = columns
    return df
