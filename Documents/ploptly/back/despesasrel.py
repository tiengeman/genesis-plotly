import oracledb
import pandas as pd
import openpyxl


def insert_despesasrel(collection):
  host = 'dbconnect.megaerp.online'
  porta = 4221
  servico = 'xepdb1'
  user = 'ENGEMAN'
  password = 'rNt3vOpDLS'
  oracledb.init_oracle_client(lib_dir=r'C:\instantclient_21_12')
  params = oracledb.ConnectParams(host=host, port=porta, service_name=servico)
  conn = oracledb.connect(user=user, password=password, params=params)

  cursor = conn.cursor()

  documents = []

  consulta = """
  SELECT 
        --A.ACAO_IN_CODIGO "AÇÃO"
        --,ACAO.ACAO_ST_NOME "NOME DA AÇÃO"
        --,A.CPAG_TPD_ST_CODIGO "TIPO DA NOTA"
        --,c.CCF_IN_REDUZIDO      "CENTRO DE CUSTO"
        PROJE.PRO_ST_DESCRICAO      "descricao-projeto"
        ,D.PROJ_IN_REDUZIDO       "codigo-projeto-original"
        ,A.RCB_ST_NOTA            "documento-despesa"
        ,A.AGN_IN_CODIGO          "codigo-agente-despesa"  
        ,F.AGN_ST_NOME            "descricao-agente-despesa"
        ,D.IRP_RE_VLPROP          "valor-original-despesa"
        ,(SELECT PC.CLA_IN_REDUZIDO
                    FROM MEGA.EST_PRODUTOCLASSE@ENGEMAN PC 
                  WHERE PC.PRO_TAB_IN_CODIGO = B.PRO_TAB_IN_CODIGO
                    AND PC.PRO_PAD_IN_CODIGO = B.PRO_PAD_IN_CODIGO
                    AND PC.PRO_IN_CODIGO     = B.PRO_IN_CODIGO
                    AND PC.TPC_ST_CLASSE     = B.TPC_ST_CLASSE
                    AND PC.APL_IN_CODIGO     = B.APL_IN_CODIGO)  "codigo-classe-despesa " 
          
        ,(SELECT FC.CLA_ST_DESCRICAO
          FROM MEGA.EST_PRODUTOCLASSE@ENGEMAN PC
              ,MEGA.FIN_CLASSE@ENGEMAN FC 
        WHERE PC.PRO_TAB_IN_CODIGO = B.PRO_TAB_IN_CODIGO
          AND PC.PRO_PAD_IN_CODIGO = B.PRO_PAD_IN_CODIGO
          AND PC.PRO_IN_CODIGO     = B.PRO_IN_CODIGO
          AND PC.TPC_ST_CLASSE     = B.TPC_ST_CLASSE
          AND PC.APL_IN_CODIGO     = B.APL_IN_CODIGO
          AND PC.CLA_TAB_IN_CODIGO = FC.CLA_TAB_IN_CODIGO
          AND PC.CLA_PAD_IN_CODIGO = FC.CLA_PAD_IN_CODIGO
          AND PC.CLA_IDE_ST_CODIGO = FC.CLA_IDE_ST_CODIGO
          AND PC.CLA_IN_REDUZIDO   = FC.CLA_IN_REDUZIDO)  "descricao-classe-despesa"

        ,A.RCB_DT_MOVIMENTO "data-despesa"

        ,COALESCE (COMP.COMPL_ST_DESCRICAO, PROD.PRO_ST_DESCRICAO) AS "OBSERVAÇÕES"

  FROM MEGA.EST_RECEBIMENTO@ENGEMAN A

  --   ,EST_ITENSSOLI ITEN

  INNER JOIN MEGA.EST_ITENSRECEB@ENGEMAN B ON A.RCB_ST_NOTA       = B.RCB_ST_NOTA
    AND  A.ORG_TAB_IN_CODIGO = B.ORG_TAB_IN_CODIGO
    AND  A.ORG_PAD_IN_CODIGO = B.ORG_PAD_IN_CODIGO
    AND  A.ORG_IN_CODIGO     = B.ORG_IN_CODIGO
    AND  A.ORG_TAU_ST_CODIGO = B.ORG_TAU_ST_CODIGO
    AND  A.AGN_TAB_IN_CODIGO = B.AGN_TAB_IN_CODIGO
    AND  A.AGN_PAD_IN_CODIGO = B.AGN_PAD_IN_CODIGO
    AND  A.AGN_IN_CODIGO     = B.AGN_IN_CODIGO
    AND  A.AGN_TAU_ST_CODIGO = B.AGN_TAU_ST_CODIGO
    --AND  A.RCB_ST_NOTA       = B.RCB_ST_NOTA
    AND  A.RCB_DT_DOCUMENTO  = B.RCB_DT_DOCUMENTO

  INNER JOIN MEGA.EST_ITENSRECEB_CCF@ENGEMAN C ON B.RCB_ST_NOTA       = C.RCB_ST_NOTA
    AND  B.ORG_TAB_IN_CODIGO = C.ORG_TAB_IN_CODIGO
    AND  B.ORG_PAD_IN_CODIGO = C.ORG_PAD_IN_CODIGO
    AND  B.ORG_IN_CODIGO     = C.ORG_IN_CODIGO
    AND  B.ORG_TAU_ST_CODIGO = C.ORG_TAU_ST_CODIGO
    AND  B.AGN_TAB_IN_CODIGO = C.AGN_TAB_IN_CODIGO
    AND  B.AGN_PAD_IN_CODIGO = C.AGN_PAD_IN_CODIGO
    AND  B.AGN_IN_CODIGO     = C.AGN_IN_CODIGO
    AND  B.AGN_TAU_ST_CODIGO = C.AGN_TAU_ST_CODIGO
    --AND  B.RCB_ST_NOTA       = C.RCB_ST_NOTA
    AND  B.RCB_DT_DOCUMENTO  = C.RCB_DT_DOCUMENTO
    AND  B.RCI_IN_SEQUENCIA  = C.RCI_IN_SEQUENCIA

  INNER JOIN MEGA.EST_ITENSRECEB_PROJ@ENGEMAN D ON C.RCB_ST_NOTA       = D.RCB_ST_NOTA
    AND  C.ORG_TAB_IN_CODIGO = D.ORG_TAB_IN_CODIGO
    AND  C.ORG_PAD_IN_CODIGO = D.ORG_PAD_IN_CODIGO
    AND  C.ORG_IN_CODIGO     = D.ORG_IN_CODIGO
    AND  C.ORG_TAU_ST_CODIGO = D.ORG_TAU_ST_CODIGO
    AND  C.AGN_TAB_IN_CODIGO = D.AGN_TAB_IN_CODIGO
    AND  C.AGN_PAD_IN_CODIGO = D.AGN_PAD_IN_CODIGO
    AND  C.AGN_IN_CODIGO     = D.AGN_IN_CODIGO
    AND  C.AGN_TAU_ST_CODIGO = D.AGN_TAU_ST_CODIGO
    --AND  C.RCB_ST_NOTA       = D.RCB_ST_NOTA
    AND  C.RCB_DT_DOCUMENTO  = D.RCB_DT_DOCUMENTO
    AND  C.RCI_IN_SEQUENCIA  = D.RCI_IN_SEQUENCIA
    AND  C.IRC_IN_SEQUENCIA  = D.IRC_IN_SEQUENCIA

INNER JOIN MEGA.GLO_PROJETOS@ENGEMAN PROJE ON PROJE.PRO_IN_REDUZIDO = D.PROJ_IN_REDUZIDO
      AND D.PROJ_TAB_IN_CODIGO = PROJE.PRO_TAB_IN_CODIGO
      AND D.PROJ_PAD_IN_CODIGO = PROJE.PRO_PAD_IN_CODIGO
      AND D.PROJ_IDE_ST_CODIGO = PROJE.PRO_IDE_ST_CODIGO

  INNER JOIN MEGA.EST_PRODUTOS@ENGEMAN PROD ON B.PRO_IN_CODIGO     =  PROD.PRO_IN_CODIGO
    AND  B.PRO_TAB_IN_CODIGO =  PROD.PRO_TAB_IN_CODIGO
    AND  B.PRO_PAD_IN_CODIGO =  PROD.PRO_PAD_IN_CODIGO
    --AND  B.PRO_IN_CODIGO     =  PROD.PRO_IN_CODIGO

  INNER JOIN MEGA.GLO_AGENTES@ENGEMAN F ON A.AGN_IN_CODIGO     = F.AGN_IN_CODIGO 
    AND  A.AGN_TAB_IN_CODIGO = F.AGN_TAB_IN_CODIGO
    AND  A.AGN_PAD_IN_CODIGO = F.AGN_PAD_IN_CODIGO
    --AND  A.AGN_IN_CODIGO     = F.AGN_IN_CODIGO 
    
  INNER JOIN MEGA.GLO_ACAO@ENGEMAN ACAO ON ACAO.ACAO_IN_CODIGO = A.ACAO_IN_CODIGO
  AND ACAO.ACAO_TAB_IN_CODIGO = A.ACAO_TAB_IN_CODIGO
  AND ACAO.ACAO_PAD_IN_CODIGO = A.ACAO_PAD_IN_CODIGO
  --ACAO.ACAO_IN_CODIGO = A.ACAO_IN_CODIGO

  /*INNER JOIN MEGA.EST_PEDIDOSRECEB@ENGEMAN  PR ON PR.RCB_ST_NOTA = B.RCB_ST_NOTA
  AND PR.ORG_TAB_IN_CODIGO   = B.ORG_TAB_IN_CODIGO
  AND PR.ORG_PAD_IN_CODIGO   = B.ORG_PAD_IN_CODIGO
  AND PR.ORG_IN_CODIGO       = B.ORG_IN_CODIGO    
  AND PR.ORG_TAU_ST_CODIGO   = B.ORG_TAU_ST_CODIGO
  AND PR.AGN_TAB_IN_CODIGO   = B.AGN_TAB_IN_CODIGO
  AND PR.AGN_PAD_IN_CODIGO   = B.AGN_PAD_IN_CODIGO
  AND PR.AGN_IN_CODIGO       = B.AGN_IN_CODIGO    
  AND PR.AGN_TAU_ST_CODIGO   = B.AGN_TAU_ST_CODIGO
  --AND PR.RCB_ST_NOTA         = B.RCB_ST_NOTA      
  AND PR.RCB_DT_DOCUMENTO    = B.RCB_DT_DOCUMENTO 
  AND PR.RCI_IN_SEQUENCIA    = B.RCI_IN_SEQUENCIA */

  /*INNER JOIN MEGA.EST_SOLICPEDIDO@ENGEMAN SP ON  SP.PDC_IN_CODIGO          = PR.PDC_IN_CODIGO
    AND SP.ORG_TAB_IN_CODIGO      = PR.ORG_TAB_IN_CODIGO
    AND SP.ORG_PAD_IN_CODIGO      = PR.ORG_PAD_IN_CODIGO
    AND SP.ORG_IN_CODIGO          = PR.ORG_IN_CODIGO    
    AND SP.ORG_TAU_ST_CODIGO      = PR.ORG_TAU_ST_CODIGO
    AND SP.PDC_SER_TAB_IN_CODIGO  = PR.SER_TAB_IN_CODIGO
    AND SP.PDC_SER_IN_SEQUENCIA   = PR.SER_IN_SEQUENCIA
  --  AND SP.PDC_IN_CODIGO          = PR.PDC_IN_CODIGO
    AND SP.ITP_IN_SEQUENCIA       = PR.ITP_IN_SEQUENCIA*/

  LEFT JOIN MEGA.Est_Desccomplemento@ENGEMAN COMP ON COMP.RCB_ST_NOTA = B.RCB_ST_NOTA
    AND COMP.ORG_TAB_IN_CODIGO = B.ORG_TAB_IN_CODIGO
    AND COMP.ORG_PAD_IN_CODIGO = B.ORG_PAD_IN_CODIGO
    AND COMP.ORG_IN_CODIGO = B.ORG_IN_CODIGO
    AND COMP.ORG_TAU_ST_CODIGO = B.ORG_TAU_ST_CODIGO
    AND COMP.AGN_TAB_IN_CODIGO = B.AGN_TAB_IN_CODIGO
    AND COMP.AGN_PAD_IN_CODIGO = B.AGN_PAD_IN_CODIGO
    AND COMP.AGN_IN_CODIGO = B.AGN_IN_CODIGO
    AND COMP.AGN_TAU_ST_CODIGO = B.AGN_TAU_ST_CODIGO
    --AND COMP.RCB_ST_NOTA = B.RCB_ST_NOTA
    AND COMP.RCB_DT_DOCUMENTO = B.RCB_DT_DOCUMENTO
    AND COMP.RCI_IN_SEQUENCIA = B.RCI_IN_SEQUENCIA


  WHERE A.RCB_DT_MOVIMENTO >= '12/04/2024'
  --AND A.RCB_DR_MOVIMENTO < = ''
  AND ACAO.ACAO_IN_CODIGO != 362
  --AND A.RCB_ST_NOTA  = '48756'
  """



  for row in cursor.execute(consulta):
      document = {
          "codigo-projeto-unificado"    : "none"
          ,"descricao-projeto"          : row[0]
          ,"codigo-projeto-original"    : row[1]
          ,"documento-despesa"          : row[2]
          ,"codigo-agente-despesa"      : row[3]
          ,"descricao-agente-despesa"   : row[4]
          ,"valor-investimento-despesa" :'none'
          ,"valor-despesa"              : 'none'
          ,"valor-original-despesa"     : row[5]
          ,"codigo-classe-despesa"      : row[6]
          ,"descricao-classe-despesa"   : row[7]
          ,"data-despesa"               : row[8]
          ,"FONTE"                      : 'none'
          ,"competencia-despesa"        : 'none'
          ,"categoria-despesa"          : 'none'
          ,"OBSERVAÇÕES"                : row[9]
          ,"tipo-despesa"               : 'none'
          # ,"AÇÃO"                         : row[0]
          # ,"NOME DA AÇÃO"                 : row[1]
          # ,"TIPO DA NOTA"                 : row[2]
          # ,"CENTRO DE CUSTO"              : row[5]
          # ,"ITEM"                         : row[9]

      }

      collection.insert_one(document)