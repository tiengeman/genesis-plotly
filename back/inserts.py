import back.banco_teste

# def insere_impostos():
#     lista = []
#     colecao_cad_impostos.insert_one = [{
#     'receitatotal-impostos'             :lista[0],
#     'pisretido-impostos'                :lista[0],
#     'pispago-impostos'                  :lista[0],
#     'pistotal-impostos'                 :lista[0],
#     'percentualpis-impostos'            :lista[0],
#     'cofinsretido-impostos'             :lista[0],
#     'cofinspago-impostos'               :lista[0],
#     'cofinstotal-impostos'              :lista[0],
#     'percentualcofins-impostos'         :lista[0],
#     'CPRB R$'                           :lista[0],
#     'CPRB %'                            :lista[0],
#     'receitaoperacional-impostos'       :lista[0],
#     'despesaoperacional-impostos'       :lista[0],
#     'resultadooperacional-impostos'     :lista[0],
#     'CSLL'                              :lista[0],
#     'IRPJ'                              :lista[0],
#     'datafechamento-impostos'           :lista[0],
#     'competencia-impostos'              :lista[0]
#     }]


def inserir_contrato(lista,db=back.db):
    colecao = db.get_collection('Cadastro Contratos')

    colecao.insert_one = [{
        'os-contratos'              :lista[0],
        'tipo-contratos'            :lista[1],
        'enquadramento-contratos'   :lista[2],
        'cliente-contratos'         :lista[3],
        'descricao-contratos'       :lista[4],
        'icj-contratos'             :lista[5],
        'sap-contratos'             :lista[6],
        'inicio-contratos'          :lista[7],
        'fim-contratos'             :lista[8],
        'aditivos-contratos'        :lista[9],
        'valor-contratos'           :lista[1],
        'prazomes-contratos'        :lista[11],
        'prazodias-contratos'       :lista[12],
        'status-contratos'          :lista[13],
        'responsavel-contratos'     :lista[14],
        'filial-contratos'          :lista[15],
        'projeto-contratos'         :lista[16],
        'projetosapiens-contratos'  :lista[17],
        'iss-contrato'              :lista[18],
        'admcentral-contrato'       :lista[19],
        'pis-contrato'              :lista[20],
        'cofins-contrato'           :lista[21],
        'csll-contrato'             :lista[22],
        'irpj-contrato'             :lista[23],
        'icms-contrato'             :lista[24],
        'investimento-contrato'     :lista[25]
    }]