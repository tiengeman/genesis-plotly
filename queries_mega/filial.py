import oracledb
import pandas as pd
import openpyxl


def pega_filiais():
  host = 'dbconnect.megaerp.online'
  porta = 4221
  servico = 'xepdb1'
  user = 'ENGEMAN'
  password = 'rNt3vOpDLS'
  oracledb.init_oracle_client(lib_dir=r'C:\instantclient_21_12')
  params = oracledb.ConnectParams(host=host, port=porta, service_name=servico)
  conn = oracledb.connect(user=user, password=password, params=params)

  cursor = conn.cursor()

  filiais = []

  consulta = """
    select agn_in_codigo "Código Filial"
       ,agn_st_fantasia "Nome Filial"
       , pa_st_sigla "País Filial"
       , uf_st_sigla "Estado Filial"
       , mun_in_codigo "Código Município Filial"
       , agn_st_municipio "Município Filial"
       , agn_st_cgc "CNPJ Filial"
       , agn_st_inscrestadual "Inscrição Estadual"

from mega.glo_agentes@engeman

where agn_bo_consolidador = 'F'
      and agn_st_fantasia != 'FILIAL - TESTE'
"""

  for filial in cursor.execute(consulta):
    filiais.append(filial)

  
  return filiais


retorno = pega_filiais()

print(retorno)